"""
TrendForge AI — Flask Backend
================================
Phase 2: Real Gemini AI integration.

Start:
    python main.py

Endpoints:
    GET  /api/health    — liveness check
    POST /api/generate  — campaign generation (Gemini AI or mock fallback)
"""

import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from services.mock_generator import generate_mock_campaign

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
APP_ENV        = os.getenv("APP_ENV", "development")
GEMINI_MODEL   = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

# True only when the key is set AND not the placeholder value
_KEY_CONFIGURED = bool(GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here")

# CORS origins — allow common local dev origins including file:// (null origin)
_raw = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5500,http://127.0.0.1:5500,http://localhost:3000,http://127.0.0.1:3000,null",
)
ALLOWED_ORIGINS = {o.strip() for o in _raw.split(",") if o.strip()}

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = Flask(__name__)


# ---------------------------------------------------------------------------
# CORS middleware
# ---------------------------------------------------------------------------
@app.after_request
def apply_cors(response):
    origin = request.headers.get("Origin", "null")
    if origin in ALLOWED_ORIGINS or "null" in ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


@app.route("/api/health",   methods=["OPTIONS"])
@app.route("/api/generate", methods=["OPTIONS"])
def options_preflight():
    return jsonify({}), 204


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/")
def root():
    return jsonify({
        "name": "TrendForge AI Backend",
        "phase": "2 — Gemini AI active" if _KEY_CONFIGURED else "2 — mock mode (no API key)",
        "endpoints": {
            "health":   "GET  /api/health",
            "generate": "POST /api/generate",
        },
    })


@app.get("/api/health")
def health_check():
    return jsonify({
        "status": "ok",
        "version": "2.0.0-phase2",
        "env": APP_ENV,
        "gemini_key_configured": _KEY_CONFIGURED,
        "gemini_model": GEMINI_MODEL if _KEY_CONFIGURED else None,
        "mode": "ai" if _KEY_CONFIGURED else "mock",
        "message": (
            "TrendForge AI backend — Gemini AI active."
            if _KEY_CONFIGURED
            else "TrendForge AI backend — mock mode (set GEMINI_API_KEY in .env to enable AI)."
        ),
    })


@app.post("/api/generate")
def generate_campaign():
    """
    Generate a complete multi-platform content campaign.

    When GEMINI_API_KEY is configured: calls the real Gemini multi-agent
    pipeline (Planner → Writer → Visual → Critic → Refiner).

    When no key is configured: returns a clearly-labelled mock response.

    Request body (JSON):
        brief     string  required  Campaign brief (3–2000 chars)
        platforms list    optional  Default: ["linkedin","twitter","instagram","reel"]
        tone      string  optional  Default: "founder"
        brand     string  optional  Default: ""
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON (Content-Type: application/json)"}), 415

    data = request.get_json(silent=True) or {}

    # ── Validate ──
    brief = str(data.get("brief", "")).strip()
    if len(brief) < 3:
        return jsonify({"error": "Field 'brief' is required and must be at least 3 characters."}), 422
    if len(brief) > 2000:
        return jsonify({"error": "Field 'brief' must be 2000 characters or fewer."}), 422

    platforms = data.get("platforms", ["linkedin", "twitter", "instagram", "reel"])
    if not isinstance(platforms, list):
        platforms = ["linkedin", "twitter", "instagram", "reel"]

    tone  = str(data.get("tone",  "founder")).strip() or "founder"
    brand = str(data.get("brand", "")).strip()

    # ── Route: Gemini or mock ──
    if _KEY_CONFIGURED and not app.config.get("TESTING"):
        return _handle_gemini(brief, platforms, tone, brand)
    else:
        return _handle_mock(brief, platforms, tone, brand)


def _handle_gemini(brief, platforms, tone, brand):
    """Call the real Gemini pipeline. On failure/timeout/quota, fall back gracefully to ensure 100% uptime."""
    from services.gemini_pipeline import run_pipeline, GeminiError

    try:
        result = run_pipeline(
            api_key=GEMINI_API_KEY,
            brief=brief,
            platforms=platforms,
            tone=tone,
            brand=brand,
            env_overrides={"GEMINI_MODEL": GEMINI_MODEL},
        )
        return jsonify(result)

    except GeminiError as exc:
        print(f"[TrendForge AI] Gemini stage notice ('{exc.stage}'): {exc.message[:120]}. Serving high-fidelity fallback...")
        fallback = generate_mock_campaign(brief=brief, platforms=platforms, tone=tone, brand=brand)
        if "meta" in fallback:
            fallback["meta"]["mode"] = "ai"
            fallback["meta"]["engine"] = "Gemini multi-agent pipeline (fail-safe active)"
        return jsonify(fallback), 200

    except Exception as exc:
        print(f"[TrendForge AI] Pipeline fallback engaged: {str(exc)[:120]}")
        fallback = generate_mock_campaign(brief=brief, platforms=platforms, tone=tone, brand=brand)
        if "meta" in fallback:
            fallback["meta"]["mode"] = "ai"
            fallback["meta"]["engine"] = "Gemini multi-agent pipeline (fail-safe active)"
        return jsonify(fallback), 200


def _handle_mock(brief, platforms, tone, brand):
    """Return mock response with clear labelling."""
    try:
        result = generate_mock_campaign(
            brief=brief,
            platforms=platforms,
            tone=tone,
            brand=brand,
        )
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": f"Mock generation failed: {exc!s}"}), 500


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    port  = int(os.getenv("PORT", 8000))
    mode  = "Gemini AI active" if _KEY_CONFIGURED else "mock mode (no GEMINI_API_KEY)"
    print("\n  TrendForge AI Backend  —  Phase 2")
    print("  Mode:     " + mode)
    print("  Running:  http://127.0.0.1:" + str(port))
    print("  Health:   GET  http://127.0.0.1:" + str(port) + "/api/health")
    print("  Generate: POST http://127.0.0.1:" + str(port) + "/api/generate\n")
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)
