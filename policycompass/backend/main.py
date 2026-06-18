import uuid
from fastapi import FastAPI, HTTPException
from .schemas import CompareRequest, ComparisonOut
from .database import async_session, engine, Base
from .models import Comparison
from .tasks import queue, run_comparison_job
import os

app = FastAPI(title="PolicyCompass")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/api/compare", response_model=ComparisonOut)
async def create_comparison(req: CompareRequest):
    async with async_session() as session:
        comp = Comparison(policy_a=req.policy_a, policy_b=req.policy_b, status="queued")
        session.add(comp)
        await session.commit()
        await session.refresh(comp)
        queue.enqueue(run_comparison_job, str(comp.id))
        return ComparisonOut.model_validate(comp)

@app.get("/api/comparison/{comp_id}", response_model=ComparisonOut)
async def get_comparison(comp_id: str):
    async with async_session() as session:
        comp = await session.get(Comparison, comp_id)
        if not comp:
            raise HTTPException(status_code=404, detail="Comparison not found")
        return ComparisonOut.model_validate(comp)
