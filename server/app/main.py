from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid

# ----- Models -----
class AgentCreate(BaseModel):
    name: str
    personality: str
    instructions: str
    task: str
    id: Optional[str] = None  # optional now, backend generates if missing

# ----- App -----
app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

agents_db = {}  # id -> agent dict

# ----- CRUD -----
@app.get("/agents")
def list_agents():
    return list(agents_db.values())

@app.post("/agents")
def create_agent(agent: AgentCreate):
    agent_id = agent.id or str(uuid.uuid4())  # generate id if missing
    agent_data = {"id": agent_id, **agent.dict(exclude={"id"})}
    agents_db[agent_id] = agent_data
    return agent_data