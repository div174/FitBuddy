# ⚡ FitBuddy — AI Fitness Plan Generator

> **Portfolio-Ready Edition.** A high-performance, resilient fitness ecosystem powered by Google Gemini. This sample project demonstrates advanced reliability engineering with automatic model fallbacks and multi-key rotation.

---

## 💎 Elite Features

| Feature | Engineering Insight |
|---------|--------------------|
| 🏋️ **AI Training** | Science-backed 7-day weekly plans generated via Gemini Flash. |
| 🛡️ **Ultra-Reliability** | **Key Rotation System**: Cycles through multiple Gemini API keys automatically. |
| 🚀 **High Availability** | **Model Fallback Chain**: 8B Flash → 2.0 Flash → 1.5 Flash → 1.5 Pro. |
| 📦 **Smart Caching** | Plans are cached in SQLite to prevent redundant API calls & save quota. |
| 💬 **Coach 2.0** | Context-aware AI coach with real-time memory and chat history. |
| 🔄 **User Feedback** | Dynamic plan refinement based on natural language feedback. |
| 🏛️ **Clean Architecture** | Modern async FastAPI backend with clean separation of concerns. |

---

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python 3.11+) - Async execution for maximum speed.
- **AI Engine:** Google Gemini SDK with custom multi-model orchestrator.
- **Database:** SQLite with SQLAlchemy (Asyncio) – Efficient persistence & caching.
- **Frontend:** Glassmorphic Neon UI – Vanilla CSS with no bloated frameworks.
- **Validation:** Pydantic v2.

---

## 🚀 Quick Start (Production Setup)

### 1. Installation
```bash
git clone https://github.com/yourusername/fitbuddy.git
cd fitbuddy
python -m venv venv
# Activate (Windows: venv\Scripts\activate | Unix: source venv/bin/activate)
pip install -r requirements.txt
cp .env.example .env
```

### 2. Configure Your API Cluster
To ensure 100% uptime, you can provide one or many Gemini keys in your `.env`. 
Get free keys at [aistudio.google.com](https://aistudio.google.com/app/apikey).

```env
# Single Key:
GOOGLE_API_KEY=AIzaSy...
# Multi-Key Rotation (Professional):
# GOOGLE_API_KEY=key1,key2,key3
```

### 3. Initialize & Run
```bash
python run.py
```
Visit: **http://localhost:8000**

---

## 📁 Project Structure

```
fitbuddy/
├── app/
│   ├── __init__.py
│   ├── config.py        # Settings loaded from .env
│   ├── main.py          # FastAPI routes & app setup
│   ├── db.py            # SQLAlchemy models & async DB helpers
│   ├── ai.py            # All Gemini API interactions
│   └── schemas.py       # Pydantic request/response models
├── templates/
│   ├── base.html        # Master layout (navbar, footer)
│   ├── index.html       # Landing page + multi-step intake form
│   ├── result.html      # Full plan view (tabs: workout/diet/tips/progress/chat)
│   └── all_plans.html   # Dashboard showing all generated plans
├── static/
│   ├── css/style.css    # Complete design system
│   └── js/app.js        # UI utilities
├── tests/
│   └── test_ai.py       # Unit tests for AI service
├── run.py               # Dev server launcher
├── .env.example         # Environment template
├── requirements.txt
└── README.md
```

---

## 🔑 API Key Security

The Gemini API key is stored **only in `.env`** on your server. It is:
- Never exposed in HTML, JS, or responses
- Never entered by users
- Loaded via `python-dotenv` at startup

This is the correct pattern for server-rendered web applications.

---

## 🌐 API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Home page with intake form |
| `POST` | `/generate` | Generate a new fitness plan |
| `POST` | `/feedback` | Refine plan with user feedback |
| `GET` | `/plan/{id}` | View a specific plan |
| `GET` | `/plans` | All generated plans |
| `POST` | `/api/progress` | Log weight & streak (JSON) |
| `POST` | `/api/chat` | AI coach chat (JSON) |
| `GET` | `/health` | Health check |

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 🚢 Deployment

### Railway / Render / Fly.io

1. Set `GEMINI_API_KEY` as an environment variable in your platform
2. Set the start command to: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feat/your-feature`
3. Commit: `git commit -m "feat: your feature"`
4. Push & open a Pull Request

---

## 📄 License

MIT — see [LICENSE](LICENSE)

---

<p align="center">Built with ⚡ and 💪 · Powered by <a href="https://deepmind.google/technologies/gemini/">Google Gemini</a></p>
