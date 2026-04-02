# app/models.py
from pydantic import BaseModel

class AgentRequest(BaseModel):
    personality: str
    instructions: str
    task: str

class AgentResponse(BaseModel):
    result: str