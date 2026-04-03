# models.py — single source of truth
from pydantic import BaseModel
from typing import Optional

class AgentRequest(BaseModel):
    personality: str
    instructions: str
    task: str

class AgentResponse(BaseModel):
    result: str

class AgentCreate(BaseModel):
    name: str
    personality: str
    instructions: str
    task: str
    id: Optional[str] = None  # backend generates if omitted

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    personality: Optional[str] = None
    instructions: Optional[str] = None
    task: Optional[str] = None