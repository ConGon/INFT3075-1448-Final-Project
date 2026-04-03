# ai_runner.py
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-r1:8b"

def run_agent(personality: str, instructions: str, task: str) -> str:
    prompt = f"Personality: {personality}\nInstructions: {instructions}\nTask: {task}"
    payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "No response from model.")  # ✅ fixed key
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Ollama: {e}"
    except (KeyError, IndexError):
        return "Unexpected response from Ollama."