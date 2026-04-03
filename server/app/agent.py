# app/agent.py
import requests
from app.models import AgentRequest

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-r1:8b"

def run_agent(data: AgentRequest) -> str:
    # Build the prompt based on personality, instructions, and task
    prompt = f"Personality: {data.personality}\nInstructions: {data.instructions}\nTask: {data.task}"

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        # Ollama returns {"results": [{"content": "..."}]}
        return result["results"][0]["content"]
    except requests.exceptions.RequestException as e:
        print("Error communicating with Ollama:", e)
        return f"Error: {str(e)}"