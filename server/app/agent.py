# server/app/agent.py
import requests

def run_agent(data: dict):
    """
    data = {
        "personality": "Strict teacher",
        "instructions": "Be concise",
        "task": "Explain recursion"
    }
    """
    prompt = f"Personality: {data['personality']}\nInstructions: {data['instructions']}\nTask: {data['task']}"
    
    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",  # Ollama endpoint
            json={
                "model": "deepseek-r1:8b",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        # Always return a readable error
        return {"error": str(e)}