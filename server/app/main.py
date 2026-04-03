from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid
import httpx

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

# ----- AI Runner -----
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-r1:8b"

async def run_agent(personality: str, instructions: str, task: str) -> str:
    prompt = f"Personality: {personality}\nInstructions: {instructions}\nTask: {task}"
    payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
    try:
        async with httpx.AsyncClient(timeout=360) as client:
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "No response from model.")
    except httpx.TimeoutException:
        return "Model timed out. Try a shorter prompt."
    except Exception as e:
        return f"Error communicating with Ollama: {e}"

@app.post("/run-agent", response_model=AgentResponse)
async def run(request: AgentRequest):
    result = await run_agent(request.personality, request.instructions, request.task)
    return {"result": result}