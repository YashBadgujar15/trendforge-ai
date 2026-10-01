# TrendForge AI — Backend

A **Flask** API that powers the TrendForge AI Content Studio.
It supports two modes: **AI mode** (Gemini 2.0 Flash via google-genai) and **Mock mode** (instant deterministic responses for demos and testing).

---

## Requirements

- Python 3.9 – 3.14
- pip

> **No pydantic, no FastAPI** — pure Flask to avoid Rust/MSVC compile issues on Windows.

---

## Setup

```bash
cd trendforge-ai/backend

# Create virtual environment (first time only)
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Configuration

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|---|---|---|
| `GEMINI_API_KEY` | *(empty)* | Your Google AI Studio key — leave blank for Mock mode |
| `GEMINI_MODEL` | `gemini-2.0-flash` | Gemini model to use |
| `PORT` | `8000` | Port to listen on |
| `ALLOWED_ORIGINS` | `*` | CORS origins (comma-separated) |

> If `GEMINI_API_KEY` is empty or missing, the server starts in **Mock mode** and returns deterministic demo data instantly.

---

## Running the server

```bash
# From trendforge-ai/backend/ with venv active:
python main.py
```

Server starts at `http://localhost:8000`.

---

## API Reference

### `GET /api/health`

Returns server status and current mode.

**Response:**
```json
{
  "status": "ok",
  "mode": "ai",        // "ai" or "mock"
  "model": "gemini-2.0-flash",
  "version": "2.0.0"
}
```

---

### `POST /api/generate`

Generates a full multi-platform campaign from a brief.

**Request body:**
```json
{
  "brief": "Launching a SaaS tool for indie developers...",
  "platforms": ["linkedin", "twitter", "instagram", "reel"],
  "tone": "Founder"
}
```

**Response** (top-level fields):
```json
{
  "meta": {
    "mode": "ai",
    "brief": "...",
    "title": "...",
    "qualityScore": 88,
    "generationTimeMs": 12400,
    "generatedAt": "2025-01-01T12:00:00Z"
  },
  "title": "...",
  "qualityScore": 88,
  "linkedin": { "hook": "...", "body": "...", "cta": "...", "chars": 1200 },
  "twitter": [{ "num": 1, "text": "...", "chars": 240 }, ...],
  "carousel": [{ "slide": 1, "type": "HOOK", "headline": "...", "subtext": "...", ... }, ...],
  "reel": { "duration": "30s", "scenes": [{ "time": "0-5s", "type": "HOOK", ... }, ...] },
  "critic": {
    "scores": {
      "humanLikeness": 85, "hookStrength": 90, "platformFit": 88,
      "brandConsistency": 82, "clarity": 87, "ctaStrength": 84, "aiSlopRisk": "LOW"
    },
    "detectedPhrases": [],
    "issues": [],
    "overallVerdict": "..."
  },
  "trace": [{ "agent": "Planner", "input": "...", "decision": "...", "output": "..." }, ...]
}
```

**Error response (4xx/5xx):**
```json
{ "error": "Brief is required" }
```

---

## Running tests

```bash
# From trendforge-ai/backend/ with venv active:
pip install pytest
pytest tests/ -v
```

Tests cover:
- Health endpoint structure
- Request validation (missing/empty brief, bad JSON)
- Full response schema validation (all required keys present)
- LinkedIn, Twitter, carousel, reel, critic structure
- Mock mode routing via `_KEY_CONFIGURED` flag
- CORS preflight

---

## Project structure

```
backend/
├── main.py                  # Flask app, routes, CORS, key detection
├── requirements.txt         # flask, python-dotenv, google-genai, flask-cors
├── .env.example             # Environment variable template
├── services/
│   ├── __init__.py
│   ├── mock_generator.py    # Phase 1 — instant deterministic mock responses
│   └── gemini_pipeline.py   # Phase 2 — 5-stage Gemini AI pipeline
└── tests/
    └── test_backend.py      # pytest test suite
```

---

## AI Pipeline (Phase 2)

When `GEMINI_API_KEY` is configured, `gemini_pipeline.py` runs a **5-stage multi-agent pipeline**:

1. **Planner** — analyzes brief, defines audience and platform strategy
2. **Writer** — generates LinkedIn post and X/Twitter thread
3. **Visual** — creates carousel slide specs and reel storyboard
4. **Critic** — scores outputs, detects AI slop phrases, flags issues
5. **Refiner** — applies critic feedback, replaces flagged phrases

Each stage's input/decision/output is captured in the `trace` array for full auditability.
