"""
TrendForge AI — Mock Generator Service
---------------------------------------
Returns a DEMO_CAMPAIGN-shaped response without calling any external API.
This is the Phase 1 placeholder. The Gemini agent pipeline will replace
generate_mock_campaign() in Phase 2 while keeping the same return schema.

IMPORTANT: No API keys are used here. This is pure Python data construction.
"""

import time
from datetime import datetime, timezone
from typing import Dict, List


# ---------------------------------------------------------------------------
# Mock content data — same structure the frontend DEMO_CAMPAIGN uses.
# When Phase 2 arrives, this data will come from Gemini instead.
# ---------------------------------------------------------------------------

_MOCK_LINKEDIN = {
    "hook": "I spent 6 years debugging my posture. Then I built the chair that fixes it for developers like me.",
    "body": (
        "Most remote developers don't have a back problem. They have a chair problem.\n\n"
        "After 6 years of coding 10+ hours a day, I realized my setup was silently "
        "destroying my productivity — not because of bad tools, but because of a bad chair.\n\n"
        "So we built something different.\n\n"
        "Introducing the DevChair Pro — the first ergonomic chair engineered specifically "
        "for developers:\n\n"
        "→ Adaptive lumbar that adjusts to your coding posture (not your \"meeting posture\")\n"
        "→ Built-in cable management for your setup\n"
        "→ Keyboard-tilt armrests that match wrist angles during extended typing\n"
        "→ Thermal mesh that keeps you focused, not sweating\n\n"
        "We tested it with 500+ developers across 18 months. The result? Average deep-work "
        "sessions increased by 41 minutes per day.\n\n"
        "That's 170+ extra hours of focused coding per year. Per developer.\n\n"
        "The best code is written by developers who aren't fighting their environment.\n\n"
        "Your setup should work for you — not against you.\n\n"
        "👉 Early access opens next week. Comment \"CHAIR\" and I'll send the link directly."
    ),
    "cta": "Comment 'CHAIR' below for early access.",
    "chars": 1247,
    "platform_compliant": True,
}

_MOCK_TWITTER = [
    {
        "num": 1,
        "text": (
            "I spent 6 years building software and silently destroying my back.\n\n"
            "Then I realized: most developer ergonomics advice is completely wrong.\n\n"
            "Here's what actually works for engineers who code 8+ hours daily 🧵"
        ),
        "chars": 224,
    },
    {
        "num": 2,
        "text": (
            "The problem isn't just sitting — it's how *developers* sit.\n\n"
            "We lean forward during debugging.\n"
            "We slump during Zoom calls.\n"
            "We shift constantly while reading code.\n\n"
            "Generic ergonomic chairs aren't designed for any of this."
        ),
        "chars": 221,
    },
    {
        "num": 3,
        "text": (
            "After 18 months of testing with 500+ developers, we found:\n\n"
            "• 73% experienced daily back or neck discomfort\n"
            "• 61% said it affected their focus after hour 4\n"
            "• 89% had never adjusted their lumbar support\n\n"
            "The chair industry has failed developers."
        ),
        "chars": 245,
    },
    {
        "num": 4,
        "text": (
            "So we built DevChair Pro — engineered from the ground up for developer workflows:\n\n"
            "→ Adaptive lumbar for coding posture (not meeting posture)\n"
            "→ Keyboard-angle armrests\n"
            "→ Built-in cable routing\n"
            "→ Thermal mesh back panel\n\n"
            "Not a \"gaming chair\" in disguise."
        ),
        "chars": 252,
    },
    {
        "num": 5,
        "text": (
            "The result? Developers using DevChair Pro averaged 41 more minutes of "
            "deep-work per day.\n\n"
            "That's 170+ extra focused hours per year.\n\n"
            "Your setup is your competitive advantage.\n\n"
            "Early access next week → RT to save your spot 🔥"
        ),
        "chars": 228,
    },
]

_MOCK_CAROUSEL = [
    {
        "slide": 1,
        "type": "hook",
        "headline": "Your chair is stealing your best code.",
        "subtext": "The average developer loses 41 min/day to discomfort-related distraction.",
        "bg": "#0a0a1a",
        "accent": "#6366f1",
    },
    {
        "slide": 2,
        "type": "problem",
        "headline": "Generic chairs weren't built for developers.",
        "subtext": "You code differently than you work. Your chair doesn't know that.",
        "points": [
            "Lean forward when debugging",
            "Shift postures every 20 min",
            "Type for hours, not meetings",
        ],
        "bg": "#0f0f20",
        "accent": "#8b5cf6",
    },
    {
        "slide": 3,
        "type": "insight",
        "headline": "500 developers. 18 months. One finding.",
        "subtext": "73% experience daily discomfort. 89% have never adjusted their lumbar.",
        "stats": [
            {"val": "73%", "label": "Daily discomfort"},
            {"val": "41min", "label": "Lost focus/day"},
            {"val": "89%", "label": "Never adjusted chair"},
        ],
        "bg": "#0d0d1e",
        "accent": "#6366f1",
    },
    {
        "slide": 4,
        "type": "solution",
        "headline": "Introducing DevChair Pro.",
        "subtext": "The first chair engineered for the developer workflow.",
        "features": [
            "Adaptive coding-posture lumbar",
            "Keyboard-tilt armrests",
            "Built-in cable management",
            "Thermal mesh focus panel",
        ],
        "bg": "#0a0a1a",
        "accent": "#10b981",
    },
    {
        "slide": 5,
        "type": "cta",
        "headline": "Get 170 extra hours of focus per year.",
        "subtext": "Early access opens next week.",
        "cta": "Follow + Comment 'CHAIR'",
        "bg": "#080814",
        "accent": "#6366f1",
    },
]

_MOCK_REEL = {
    "duration": "0:30",
    "scenes": [
        {
            "time": "00:00",
            "type": "HOOK",
            "visual": "Developer slouching, back pain",
            "voiceover": "What if your chair is your biggest productivity killer?",
            "text": "Your chair is costing you code.",
            "duration": "5s",
        },
        {
            "time": "00:05",
            "type": "PROBLEM",
            "visual": "Split screen: generic chair vs developer posture",
            "voiceover": "Most developers lose 41 minutes of focus every single day.",
            "text": "41 min/day. Lost to discomfort.",
            "duration": "7s",
        },
        {
            "time": "00:12",
            "type": "INSIGHT",
            "visual": "Data visualization of 500 developers",
            "voiceover": "We studied 500 engineers over 18 months.",
            "text": "500 devs. 18 months. 1 conclusion.",
            "duration": "8s",
        },
        {
            "time": "00:20",
            "type": "PRODUCT",
            "visual": "DevChair Pro reveal, slow rotation",
            "voiceover": "Introducing DevChair Pro — built for how developers actually work.",
            "text": "DevChair Pro.",
            "duration": "7s",
        },
        {
            "time": "00:27",
            "type": "CTA",
            "visual": "Clean product shot with URL overlay",
            "voiceover": "Early access next week. Link in bio.",
            "text": "Early access → Link in bio",
            "duration": "3s",
        },
    ],
}

_MOCK_CRITIC = {
    "scores": {
        "humanLikeness": 91,
        "hookStrength": 87,
        "platformFit": 94,
        "brandConsistency": 96,
        "clarity": 89,
        "ctaStrength": 82,
        "aiSlopRisk": "LOW",
    },
    "detectedPhrases": [
        "innovative solution",
        "game-changing",
        "seamless experience",
    ],
    "issues": [
        {
            "severity": "medium",
            "platform": "LinkedIn",
            "description": "Opening hook could be more specific to developer identity.",
            "action": "Regenerated with personal founder POV.",
            "status": "resolved",
        },
        {
            "severity": "low",
            "platform": "X",
            "description": "Thread #3 stats need source attribution for credibility.",
            "action": "Added qualifier 'based on internal testing'.",
            "status": "resolved",
        },
        {
            "severity": "low",
            "platform": "Carousel",
            "description": "Slide 3 text density exceeded safe visual area.",
            "action": "Reduced body copy, increased stat size.",
            "status": "resolved",
        },
    ],
    "overallVerdict": (
        "Strong campaign. Human-first voice maintained across all platforms. "
        "Anti-slop filter cleared 3 generic phrases. "
        "CTA consistency improved post-refinement."
    ),
}

_MOCK_TRACE = [
    {
        "agent": "Planner",
        "input": "Product brief: DevChair Pro for remote developers",
        "decision": "Selected LinkedIn, X, Instagram, Reel. Tone: Founder. Audience: Remote developers 25–40.",
        "output": "Campaign structure defined. 4 platform strategies queued.",
        "status": "done",
    },
    {
        "agent": "Content Generator",
        "input": "Platform strategies + brand kit",
        "decision": "LinkedIn: founder story angle. X: data-driven thread. Carousel: visual stats. Reel: hook-problem-solution arc.",
        "output": "4 platform content drafts produced.",
        "status": "done",
    },
    {
        "agent": "Visual Generator",
        "input": "Carousel brief + brand colors",
        "decision": "5 slides: hook, problem, insight, solution, CTA. Dark premium palette. Stat-forward design.",
        "output": "5 carousel slides structured. Reel storyboard built.",
        "status": "done",
    },
    {
        "agent": "Critic",
        "input": "All 4 platform drafts",
        "decision": "Detected 3 AI-slop phrases. LinkedIn hook weak. Carousel slide 3 text overflow.",
        "output": "3 issues flagged. Sent back to Refiner.",
        "status": "done",
    },
    {
        "agent": "Refiner",
        "input": "3 flagged issues from Critic",
        "decision": "LinkedIn hook rewritten with first-person founder voice. 3 slop phrases removed. Carousel slide 3 layout adjusted.",
        "output": "Refined drafts on all 3 issues.",
        "status": "done",
    },
    {
        "agent": "Final Output",
        "input": "Refined content from all agents",
        "decision": "Quality gate passed. All scores above 80. Human approval gate triggered.",
        "output": "Campaign package ready for human review.",
        "status": "done",
    },
]


# ---------------------------------------------------------------------------
# Public function called by main.py
# ---------------------------------------------------------------------------

def generate_mock_campaign(
    brief: str,
    platforms: List[str],
    tone: str,
    brand: str,
) -> Dict:
    """
    Returns a mock campaign response shaped identically to what the Gemini
    pipeline will return in Phase 2. The brief/platforms/tone/brand arguments
    are accepted but not yet used to vary the output — that happens in Phase 2.
    """
    start = time.monotonic()

    # Simulate a small processing delay so the frontend pipeline animation
    # looks realistic even against a local server.
    # Remove this in Phase 2 — real Gemini latency will replace it.
    time.sleep(0.3)

    elapsed_ms = int((time.monotonic() - start) * 1000)

    title = _derive_title(brief)
    quality_score = 91

    return {
        # ── Top-level fields (read directly by frontend) ───────────────────
        "title":        title,
        "qualityScore": quality_score,
        # ── Metadata ──────────────────────────────────────────────────────
        "meta": {
            "mode": "mock",            # "mock" | "ai" — frontend checks this
            "brief": brief,
            "platforms": platforms,
            "tone": tone,
            "brand": brand,
            "title": title,
            "qualityScore": quality_score,
            "generationTimeMs": elapsed_ms,
            "generatedAt": datetime.now(timezone.utc).isoformat(),
        },
        # ── Content ───────────────────────────────────────────────────────
        "linkedin":  _MOCK_LINKEDIN,
        "twitter":   _MOCK_TWITTER,
        "carousel":  _MOCK_CAROUSEL,
        "reel":      _MOCK_REEL,
        "critic":    _MOCK_CRITIC,
        "trace":     _MOCK_TRACE,
    }


def _derive_title(brief: str) -> str:
    """
    Produce a short campaign title from the brief.
    In Phase 2 Gemini will generate this; for now use the first 8 words.
    """
    words = brief.strip().split()
    snippet = " ".join(words[:8])
    if len(words) > 8:
        snippet += "..."
    return snippet or "Untitled Campaign"
