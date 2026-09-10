# CoreAI

CoreAI is a multi-agent backend for handling calendar, email, and task requests through a single conversational API. A supervisor agent routes each request to the right specialist agent (or chains several together for multi-step actions, like checking availability before booking a meeting), persists conversation and task state to Postgres, and integrates with Google Calendar and Gmail via OAuth.

It's a personal project built to explore agent orchestration patterns on top of a fairly standard Flask/Node/Postgres backend.

## Architecture

```
Frontend (Next.js)
        |  HTTP/REST
Node.js Proxy (Express, port 3001)
        |  Forward/Stream
Flask API (port 5000)
        |
Supervisor Agent
   |    |    |    |    |    |
Calendar Meeting Email Weather News Task
```

The Node proxy forwards requests to Flask and streams the response back; it also handles CORS and cookie forwarding for session-based auth. The Flask service does the actual work: routing requests to agents, calling external APIs (Google Calendar/Gmail, weather, news), and reading/writing Postgres.

## Setup

Requirements: Python 3.9+, Node 18+, Docker (optional, for the full stack).

### Option 1 — Docker (recommended)

```bash
git clone https://github.com/Tanaybaviskar/CoreAI.git
cd CoreAI
cp backend/agentic/.env.example backend/agentic/.env   # fill in your API keys
docker compose up --build
```

This starts Postgres, the Flask API, and the Node proxy together.

### Option 2 — run locally

```bash
cd backend/agentic
python -m venv venv
venv\Scripts\activate      # or: source venv/bin/activate on macOS/Linux
pip install -r requirements.txt
cp .env.example .env       # fill in your API keys
python main.py             # http://localhost:5000, falls back to local SQLite
```

```bash
cd backend
npm install
node index.js               # http://localhost:3001
```

```bash
cd frontend
npm install
npm run dev                 # http://localhost:3000
```

### API keys

- `GOOGLE_API_KEY` — Gemini, from [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- `SERPER_API_KEY` — web search, from [serper.dev](https://serper.dev)
- Google Calendar/Gmail OAuth client — from [Google Cloud Console](https://console.cloud.google.com), see `GOOGLE_SETUP.md`
- Weather/News API keys are optional; those agents degrade gracefully without them

## Database

Conversation history, tasks, and memory items are persisted via SQLAlchemy. `DATABASE_URL` controls the backend — set it to a Postgres URL in production/Docker, or leave it unset for a local SQLite file during development. Models are in `backend/agentic/database.py`; tables are created automatically on startup.

## Testing

```bash
cd backend/agentic
pytest tests/ -v
```

Tests run against an isolated SQLite database and cover the health check, `/invoke` request validation, task persistence, `/memory`, and `/metrics`.

## Monitoring

`GET /metrics` exposes Prometheus-format counters and latency histograms for `/invoke` requests.

## API reference

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check + agent status |
| POST | `/invoke` | Send a message, get a routed agent response |
| GET | `/agents` | List all agents and their status |
| GET/POST | `/memory` | Read/write persisted memory items |
| GET | `/activity` | Recent conversation activity |
| GET | `/metrics` | Prometheus metrics |
| GET | `/auth/login` | Start Google OAuth flow |
| GET | `/auth/status` | Check current auth state |

## Project structure

```
CoreAI/
├── frontend/                 Next.js UI
├── backend/
│   ├── index.js               Express proxy (port 3001)
│   └── agentic/                Flask API (port 5000)
│       ├── main.py
│       ├── database.py         SQLAlchemy models + session handling
│       ├── agents/             Supervisor + specialist agents
│       ├── utils/               OAuth, API clients
│       └── tests/
├── docker-compose.yml
└── backend/agentic/Dockerfile, backend/Dockerfile
```

## Known limitations

- `/invoke` streams the fully-computed response character by character rather than true token-level streaming from the LLM.
- Agent routing is keyword-based (`can_handle()`), not LLM-driven intent classification, despite LangGraph being listed as a dependency — this is the next thing I want to rework.
- No retry/backoff around external Google API calls yet.

## Tech stack

**Frontend:** Next.js, React, TypeScript, Tailwind CSS
**Backend:** Flask, LangChain, Google Gemini, Express, Axios
**Data/infra:** PostgreSQL, SQLAlchemy, Docker, Prometheus

## License

MIT