# FounderGate

**Core mission:** Give founders back their most valuable asset—**time to think**—by automating repetitive interview synthesis while forcing critical human judgment on confirmation bias.

## Development Setup

### Backend (Python 3.11+, FastAPI)

```bash
cd backend
uv venv
source .venv/bin/activate
uv pip install -e .
uvicorn main:app --reload --port 8000
```

### Frontend (Node.js 20+, Next.js)

```bash
cd frontend
pnpm install
pnpm dev
```
