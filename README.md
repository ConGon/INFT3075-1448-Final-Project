AI Agent AppA full-stack AI agent application leveraging FastAPI for the backend, Vue 3 for the interactive frontend, and Ollama as the local LLM runtime.This application allows users to configure agent personalities, set specific instructions, and execute tasks with real-time AI-generated responses.🚀 FeaturesFastAPI Backend: Robust AI agent logic and API orchestration.Vue 3 Frontend: Modern, interactive UI built with Vite.Local AI Power: Uses Ollama (deepseek-r1:8b) for private, local inference.Profile System: Dynamically add and edit agent configurations.Real-time Updates: Immediate feedback on AI processing tasks.🛠 Tech StackComponentTechnologyFrontendVue 3 + ViteBackendFastAPI (Python 3.10+)AI RuntimeOllamaModeldeepseek-r1:8b📁 Project StructurePlaintextproject-root/
│
├── server/
│   ├── app/
│   │   ├── main.py        # FastAPI entry point
│   │   ├── agent.py       # AI logic (calls Ollama)
│   │   └── models.py      # Pydantic data models
│   └── requirements.txt
│

├── client/
│   ├── src/
│   │   ├── views/         # Vue pages (Add, Edit, Testing)
│   │   └── components/    # Reusable UI components
│   └── package.json
│
└── README.md
⚙️ PrerequisitesEnsure you have the following installed:Python 3.10+Node.js (v18+ recommended)npm or pnpmOllama🔧 Setup Instructions1. Install and Run OllamaDownload and install from ollama.com.Pull the required model:Bashollama pull deepseek-r1:8b
Start the Ollama service:Bashollama serve
Test the connection (PowerShell):PowerShellInvoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"model":"deepseek-r1:8b","prompt":"Hello","stream":false}'
2. Backend Setup (FastAPI)Bashcd server
python -m venv venv

# Windows Activation
venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Run Server
uvicorn app.main:app --reload
Backend runs on: http://localhost:80003. Frontend Setup (Vue 3)Bashcd client
npm install
npm run dev
Frontend runs on: http://localhost:5173🧠 How It WorksUser Input: The user defines a Personality, Instructions, and a Task via the Vue UI.Request: The frontend sends a POST request to /run-agent.Processing: FastAPI builds the prompt and forwards it to the local Ollama API.Inference: Ollama runs the deepseek-r1:8b model and returns the text.Display: The response is piped back to the UI and displayed in the "crystal ball" interface.API Endpoint: POST /run-agentRequest Body:JSON{
  "personality": "Strict teacher",
  "instructions": "Be concise",
  "task": "Explain recursion"
}
🛠 TroubleshootingPort 11434 Busy: netstat -aon | findstr :11434 then taskkill /PID <PID> /FCORS Errors: Ensure allow_origins=["http://localhost:5173"] is configured in your FastAPI middleware.Git Security Issues: If you see "dubious ownership" errors, run:Bashgit config --global --add safe.directory 'E:/SchoolFolder/INFT(NPM)-Emerging-Technologies/Final-Project/INFT3075-1448-Final-Project'
🚀 Future Improvements[ ] Streaming: Implement Server-Sent Events (SSE) for real-time typing effects.[ ] Persistence: Add a database (SQLite/PostgreSQL) for agent profiles.[ ] Auth: Implement user login/authentication.[ ] Dynamic Models: Allow users to switch between different Ollama models in the UI.