from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid
from app.agent import run_agent

# ----- Models -----
class AgentCreate(BaseModel):
    name: str
    personality: str
    instructions: str
    task: str
    id: Optional[str] = None

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    personality: Optional[str] = None
    instructions: Optional[str] = None
    task: Optional[str] = None

class AgentRequest(BaseModel):
    personality: str
    instructions: str
    task: str
    temperature: float = 0.5

class AgentResponse(BaseModel):
    result: str

# ----- App -----
app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

agents_db = {}

# ----- CRUD -----
@app.get("/agents")
def list_agents():
    return list(agents_db.values())

@app.post("/agents")
def create_agent(agent: AgentCreate):
    agent_id = agent.id or str(uuid.uuid4())
    agent_data = {"id": agent_id, **agent.dict(exclude={"id"})}
    agents_db[agent_id] = agent_data
    return agent_data

@app.put("/agents/{agent_id}")
def update_agent(agent_id: str, agent: AgentUpdate):
    if agent_id not in agents_db:
        raise HTTPException(404, "Agent not found")
    for k, v in agent.dict().items():
        if v is not None:
            agents_db[agent_id][k] = v
    return agents_db[agent_id]

@app.delete("/agents/{agent_id}")
def delete_agent(agent_id: str):
    if agent_id not in agents_db:
        raise HTTPException(404, "Agent not found")
    del agents_db[agent_id]
    return {"message": "Deleted"}

@app.post("/run-agent", response_model=AgentResponse)
def run(request: AgentRequest):
    result = run_agent(request.personality, request.instructions, request.task, request.temperature)
    return {"result": result}