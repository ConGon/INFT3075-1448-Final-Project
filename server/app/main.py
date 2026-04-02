# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import AgentRequest, AgentResponse
from app.agent import run_agent

app = FastAPI(title="AI Agent Creator")

# Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/run-agent", response_model=AgentResponse)
def run(request: AgentRequest):
    result = run_agent(request)
    return {"result": result}

@app.get("/")
def root():
    return {"message": "AI Agent Creator API is running"}