# server/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.agent import run_agent
from pydantic import BaseModel

app = FastAPI()

# Enable CORS for Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentRequest(BaseModel):
    personality: str
    instructions: str
    task: str

@app.post("/run-agent")
def run(data: AgentRequest):
    result = run_agent(data.dict())
    return result