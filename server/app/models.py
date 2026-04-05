# models.py — single source of truth
from pydantic import BaseModel
from typing import Optional

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