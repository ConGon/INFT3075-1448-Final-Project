import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-r1:8b"

def run_agent(personality: str, instructions: str, task: str, temperature: float) -> str:
    prompt = f"""
Respond only in English.

Personality: {personality}
Instructions: {instructions}
Task: {task}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=360)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "No response from model.")
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Ollama: {e}"
    except (KeyError, IndexError):
        return "Unexpected response from Ollama."