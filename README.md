# 🤖 AI Agent App — Local LLM Orchestrator

A full-stack application for creating and executing custom AI agent personalities. Built with **FastAPI**, **Vue 3**, and **Ollama** for fully private, local inference using the `deepseek-r1:8b` model — no cloud, no API costs.

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [How It Works](#-how-it-works)
- [Troubleshooting](#-troubleshooting)
- [Future Improvements](#-future-improvements)

## 🧠 Overview

This application lets users define specialized AI agents with custom **Personalities** and **Instructions**. All inference runs on local hardware via Ollama, keeping your data private.

The core workflow follows a simple **Request → Process → Response** cycle: the Vue frontend captures agent parameters, FastAPI constructs an optimized prompt, and the DeepSeek model returns a result — all without leaving your machine.

## ✨ Features

- **Dynamic Agent Profiles** — Create, edit, and save custom agent personalities (e.g., *Strict Teacher*, *Creative Coder*)
- **Local Inference** — High-performance AI generation via Ollama (`deepseek-r1:8b`)
- **FastAPI Backend** — Async API handling with structured Pydantic data validation
- **Reactive UI** — Vue 3 + Vite for a fast, modern development experience with hot-reloading
- **Real-time Feedback** — Immediate response display via a "crystal ball" interface

## 🛠 Tech Stack

| Component  | Technology             |
|------------|------------------------|
| Frontend   | Vue 3 + Vite           |
| Backend    | FastAPI (Python 3.10+) |
| AI Runtime | Ollama                 |
| LLM Model  | deepseek-r1:8b         |
| Styling    | CSS3 / Custom UI       |

## 📁 Project Structure

```
project-root/
│
├── server/
│   ├── app/
│   │   ├── main.py          # FastAPI entry point & middleware
│   │   ├── agent.py         # AI logic & Ollama API integration
│   │   └── models.py        # Pydantic schemas for requests/responses
│   └── requirements.txt     # Python dependencies
│
├── client/
│   ├── src/
│   │   ├── views/           # Page components (Add, Edit, Testing)
│   │   ├── components/      # Reusable UI (Inputs, Crystal Ball, Buttons)
│   │   └── App.vue          # Root component
│   └── package.json         # Node scripts and dependencies
│
└── README.md
```

## ⚙️ Prerequisites

Ensure the following are installed before getting started:

- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js v18+](https://nodejs.org/) & npm
- [Ollama](https://ollama.com)

## 🔧 Installation & Setup

### 1. Configure Ollama

Pull the model and start the local inference server:

```bash
ollama pull deepseek-r1:8b
ollama serve
```

### 2. Backend Setup (FastAPI)

```bash
cd server
python -m venv venv

# Activate (Windows)
\venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

> Backend available at: `http://localhost:8000`

### 3. Frontend Setup (Vue 3)

Open a new terminal:

```bash
cd client
npm install
npm run dev
```

> Frontend available at: `http://localhost:5173`

## 🔄 How It Works

1. **User Input** — Define a *Personality*, *Instructions*, and *Task* in the Vue UI
2. **Request** — Frontend sends a `POST` to `/run-agent` with a JSON payload
3. **Processing** — FastAPI sanitizes input, builds the prompt, and forwards it to Ollama (`localhost:11434`)
4. **Inference** — Ollama runs `deepseek-r1:8b` and returns generated text
5. **Display** — Response is proxied back through FastAPI and shown in the crystal ball UI

## 🛠 Troubleshooting

**CORS Errors**
Ensure `allow_origins=["http://localhost:5173"]` is set in `main.py` under `CORSMiddleware`.

**Port 11434 Already in Use**
```powershell
netstat -aon | findstr :11434
taskkill /PID <PID> /F
```

**Git "Dubious Ownership" Error**
```bash
git config --global --add safe.directory 'E:/path/to/your/project'
```

## 🚀 Future Improvements

- [ ] **Streaming** — Server-Sent Events (SSE) for real-time "typing" effects
- [ ] **Persistence** — SQLite integration to save agent profiles permanently
- [ ] **Auth** — Lightweight user login system
- [ ] **Multi-Model** — Dropdown to switch between `llama3`, `mistral`, or `phi3`

## 📄 Licence

Open-source project created for the **INFT3075 Emerging Technologies** course.
