import json
from .database import async_session
from .models import Comparison
from .agent import run_autonomous_comparison
from sqlalchemy import update

async def process_comparison(comparison_id: str):
    async with async_session() as session:
        comp = await session.get(Comparison, comparison_id)
        if not comp:
            return
        comp.status = "processing"
        await session.commit()
        try:
            output = run_autonomous_comparison(comp.policy_a, comp.policy_b)
            try:
                result_json = json.loads(output)
            except:
                result_json = {"raw_output": output}
            comp.result = result_json
            comp.status = "completed"
        except Exception as e:
            comp.status = "failed"
            comp.result = {"error": str(e)}
        await session.commit()
