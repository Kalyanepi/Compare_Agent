import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
import json

def _get_llm():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return None
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=key)

@tool
def extract_clauses(text: str) -> dict:
    """Extract key insurance/policy clauses from raw text. Returns JSON with clause names and values."""
    llm = _get_llm()
    if not llm:
        clauses = {}
        for line in text.split('\n'):
            if ':' in line:
                k, v = line.split(':', 1)
                clauses[k.strip()] = v.strip()
        return clauses
    prompt = f"""Extract the main policy clauses (e.g., coverage amount, deductible, premium, exclusions, waiting period) from the following text. Return only a JSON object where keys are clause names and values are the clause text.\n\nText:\n{text[:3000]}"""
    resp = llm.invoke(prompt)
    try:
        return json.loads(resp.content)
    except:
        return {"raw_extract": resp.content}

@tool
def compare_clauses(clauses_a: dict, clauses_b: dict) -> str:
    """Compare two sets of policy clauses and list key differences. Returns a JSON with summary and per-clause comparison."""
    llm = _get_llm()
    if not llm:
        all_keys = set(list(clauses_a.keys()) + list(clauses_b.keys()))
        differences = []
        for k in all_keys:
            va = clauses_a.get(k, "Not specified")
            vb = clauses_b.get(k, "Not specified")
            diff = "Same" if va == vb else f"A: {va} | B: {vb}"
            differences.append({"clause": k, "policy_a_value": va, "policy_b_value": vb, "difference": diff})
        summary = "Demo mode: simple field comparison."
        return json.dumps({"summary": summary, "clauses": differences})
    prompt = f"""Compare the following two policy clause sets and identify important differences. Return a JSON with fields: "summary" (overall comparison summary), and "clauses" (array of objects: clause, policy_a_value, policy_b_value, difference).\n\nPolicy A:\n{clauses_a}\n\nPolicy B:\n{clauses_b}"""
    resp = llm.invoke(prompt)
    return resp.content

def run_autonomous_comparison(policy_a: str, policy_b: str) -> str:
    llm = _get_llm()
    if not llm:
        clauses_a = extract_clauses(policy_a)
        clauses_b = extract_clauses(policy_b)
        return compare_clauses(clauses_a, clauses_b)

    tools = [extract_clauses, compare_clauses]
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="You are an autonomous policy comparison agent. Use the tools to first extract clauses from both policies, then compare them. Provide the final comparison as a JSON."),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    result = agent_executor.invoke({"input": f"Compare these two policies.\nPolicy A:\n{policy_a[:3000]}\nPolicy B:\n{policy_b[:3000]}"})
    return result["output"]
