from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .agents import run_recovery_flow

app = FastAPI(title="Rec-Buddy API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecoveryRequest(BaseModel):
    message: str
    preference: str = "long-term"

@app.get("/")
async def root():
    return {"message": "Welcome to Rec-Buddy API"}

@app.post("/chat")
async def chat(request: RecoveryRequest):
    try:
        # Trigger the multi-agent workflow
        result = await run_recovery_flow(request.message, request.preference)
        return {
            "response": "Here is my analysis and plan based on your feedback:",
            "diagnosis": result["diagnosis"],
            "recovery_plan": result["recovery_plan"],
            "safety_check": result["safety_check"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
