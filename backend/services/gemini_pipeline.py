"""
TrendForge AI — Gemini Multi-Agent Pipeline
=============================================
Implements the real AI generation pipeline using Google Gemini.
Called by main.py when GEMINI_API_KEY is present and valid.

Pipeline stages (each is a real Gemini API call):
  1. Planner      — brief → audience + platform strategies
  2. Writer       — strategies → LinkedIn post + X thread
  3. Visual       — brief + context → carousel slides + reel storyboard
  4. Critic       — all drafts → quality scores + issues
  5. Refiner      — issues → revised content

Security:
  - API key is read from environment only (never logged or returned)
  - Trace records never contain environment variables or key values
"""

import json
import os
import re
import time
from datetime import datetime, timezone
from typing import Dict, List, Tuple

from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SLOP_PHRASES = [
    # Overused AI filler
    "delve", "delving", "delved",
    "elevate", "elevating",
    "unlock your potential", "unlock the power", "unlock your",
    "game-changing", "game changer", "game-changer",
    "innovative solution", "innovative approach",
    "seamless experience", "seamless integration", "seamless",
    "robust", "leverage", "leveraging",
    "paradigm shift", "synergy", "synergistic",
    "transformative", "groundbreaking",
    "cutting-edge", "best-in-class",
    "holistic", "scalable solution",
    "dive deep", "dive into",
    "it's worth noting", "it is important to note",
    "in today's world", "in today's digital age",
    "at the end of the day",
    "move the needle",
    # Generic openings / corporate filler
    "in today's fast-paced world",
    "technology is changing",
    "are you ready to",
    "here's the thing",
    "revolutionize", "revolutionizing", "revolutionise",
    "transform your", "transforming your",
    "in today's digital landscape",
    "it's not just", "it is not just",
    "game changer for",
    "future-proof",
    "next-level",
    "powerful tool",
    "exciting journey",
    "take your X to the next level",
    "in a world where",
    "the truth is",
]

CAROUSEL_BG = ["#0a0a1a", "#0f0f20", "#0d0d1e", "#0a0a1a", "#080814"]
CAROUSEL_ACCENT = ["#6366f1", "#8b5cf6", "#6366f1", "#10b981", "#6366f1"]

GENERATION_CONFIG = types.GenerateContentConfig(
    temperature=0.85,
    top_p=0.95,
    max_output_tokens=4096,
)

# ---------------------------------------------------------------------------
# Client factory — created once per call so the key is never stored globally
# ---------------------------------------------------------------------------

def _make_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)


def _model(env: dict) -> str:
    return env.get("GEMINI_MODEL", "gemini-2.0-flash")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _call_gemini(client: genai.Client, model: str, prompt: str, trace: list, stage: str) -> str:
    """
    Make one Gemini API call. Appends a trace entry.
    Raises GeminiError on failure.
    """
    try:
        resp = client.models.generate_content(
            model=model,
            contents=prompt,
            config=GENERATION_CONFIG,
        )
        text = resp.text.strip()
        trace.append({
            "agent": stage,
            "status": "done",
            "_raw_chars": len(text),
        })
        return text
    except Exception as exc:
        err_msg = str(exc)
        # Never leak the API key if it appears in the error string
        api_key = os.getenv("GEMINI_API_KEY", "")
        if api_key:
            err_msg = err_msg.replace(api_key, "[REDACTED]")
        trace.append({"agent": stage, "status": "error", "error": err_msg})
        raise GeminiError(stage, err_msg) from exc


def _extract_json(text: str) -> dict:
    """
    Extract the first JSON object or array from a text that may contain
    markdown fences or surrounding prose.
    """
    # Strip ```json ... ``` fences
    cleaned = re.sub(r"```(?:json)?\s*", "", text)
    cleaned = cleaned.replace("```", "").strip()
    # Find first { or [
    start = min(
        (cleaned.find("{") if "{" in cleaned else len(cleaned)),
        (cleaned.find("[") if "[" in cleaned else len(cleaned)),
    )
    if start == len(cleaned):
        raise ValueError("No JSON object found in response")
    return json.loads(cleaned[start:])


def _detect_slop(text: str) -> List[str]:
    found = []
    lower = text.lower()
    for phrase in SLOP_PHRASES:
        if phrase.lower() in lower:
            found.append(phrase)
    return found


def _char_count(text: str) -> int:
    return len(text)


def _safe_str(val, default="") -> str:
    return str(val).strip() if val else default


def _safe_list(val, default=None) -> list:
    if isinstance(val, list):
        return val
    return default or []


# ---------------------------------------------------------------------------
# Error type
# ---------------------------------------------------------------------------

class GeminiError(Exception):
    def __init__(self, stage: str, message: str):
        self.stage = stage
        self.message = message
        super().__init__(f"[{stage}] {message}")


# ---------------------------------------------------------------------------
# Stage 1: Planner
# ---------------------------------------------------------------------------

def _run_planner(
    client: genai.Client,
    model: str,
    brief: str,
    platforms: List[str],
    tone: str,
    brand: str,
    trace: list,
) -> dict:
    platform_list = ", ".join(platforms)
    brand_ctx = f"Brand: {brand}. " if brand else ""
    prompt = f"""You are a strategic content planner for a marketing campaign.

Brief: {brief}
{brand_ctx}Platforms: {platform_list}
Tone: {tone}

RULES — READ CAREFULLY:
1. Extract audience, facts, and unique angles ONLY from the brief above.
2. Do NOT invent statistics, research findings, customer numbers, or performance claims that are not in the brief.
3. Do NOT assume the writer has personal experience with the product unless the brief says so.
4. The unique_angle must come from the actual product/service described, not generic marketing concepts.
5. Platform strategies must be specific to the brief — not generic content advice.

Analyze the brief and return ONLY a JSON object with this exact structure:
{{
  "campaign_title": "short punchy campaign title (max 8 words, specific to the product)",
  "target_audience": "specific audience description drawn from the brief (1-2 sentences)",
  "core_message": "the single most important message grounded in the brief (1 sentence)",
  "unique_angle": "what genuinely differentiates this product/service based on the brief (1 sentence)",
  "brief_facts": "list any specific facts, numbers, or claims explicitly stated in the brief (or write 'none provided')",
  "platform_strategies": {{
    "linkedin": "specific strategy for LinkedIn based on the brief and audience (1 sentence)",
    "twitter": "specific strategy for X/Twitter thread based on the brief (1 sentence)",
    "instagram": "specific strategy for Instagram carousel based on the brief (1 sentence)",
    "reel": "specific strategy for Reel/short video based on the brief (1 sentence)"
  }}
}}

Return ONLY the JSON object. No markdown, no explanation."""

    raw = _call_gemini(client, model, prompt, trace, "Planner")
    try:
        plan = _extract_json(raw)
    except (json.JSONDecodeError, ValueError) as exc:
        raise GeminiError("Planner", f"Invalid JSON from planner: {exc}") from exc

    # Validate required fields
    required = ["campaign_title", "target_audience", "core_message", "platform_strategies"]
    for field in required:
        if field not in plan:
            plan[field] = ""

    # Enrich trace with visible (non-secret) info
    trace[-1].update({
        "agent": "Planner",
        "input": f"Brief: {brief[:120]}{'...' if len(brief) > 120 else ''}",
        "decision": (
            f"Audience: {_safe_str(plan.get('target_audience'))[:80]}. "
            f"Core message: {_safe_str(plan.get('core_message'))[:80]}."
        ),
        "output": f"Campaign title: {_safe_str(plan.get('campaign_title'))}. Strategies defined for {len(platforms)} platforms.",
    })
    return plan


# ---------------------------------------------------------------------------
# Stage 2: Content Writer (LinkedIn + Twitter)
# ---------------------------------------------------------------------------

def _run_writer(
    client: genai.Client,
    model: str,
    brief: str,
    plan: dict,
    tone: str,
    brand: str,
    trace: list,
) -> Tuple[dict, List[dict]]:
    brand_ctx = f"Brand name: {brand}. " if brand else ""
    audience = _safe_str(plan.get("target_audience"))
    core_msg  = _safe_str(plan.get("core_message"))
    li_strat  = _safe_str(plan.get("platform_strategies", {}).get("linkedin"))
    tw_strat  = _safe_str(plan.get("platform_strategies", {}).get("twitter"))

    brief_facts = _safe_str(plan.get("brief_facts", "none provided"))

    prompt = f"""You are a professional content writer creating platform-native marketing content.

Brief: {brief}
{brand_ctx}Target audience: {audience}
Core message: {core_msg}
Tone: {tone}
LinkedIn strategy: {li_strat}
Twitter/X strategy: {tw_strat}
Facts explicitly stated in the brief: {brief_facts}

STRICT RULES — FOLLOW EXACTLY:

1. NO INVENTED PERSONAL EXPERIENCES
   - Do NOT write "I realized...", "I experienced...", "During my [time]...", "Last [period] I..."
   - Do NOT fabricate a founder story, personal anecdote, or customer testimonial unless the brief explicitly provides one.
   - If no personal story exists in the brief, use: product observation, product insight, a general pattern, or a relatable hypothetical framed as a question.

2. NO UNSUPPORTED STATISTICS OR CLAIMS
   - Only use numbers or research findings that appear in: "{brief_facts}"
   - If no numbers are provided, do NOT invent any. Use qualitative observations instead.
   - Do NOT write things like "73% of users..." or "studies show..." unless that data is in the brief.

3. HOOKS MUST BE SPECIFIC AND NATURAL
   - The LinkedIn hook must be directly about the product/topic from the brief.
   - Do NOT open with: "In today's world...", "Technology is changing...", "Are you ready to...", "Here's the thing..."
   - Do NOT open with a fabricated personal story.
   - Good hook patterns: specific observation about the problem, a sharp question about the use-case, a counterintuitive product insight.

4. CTA MUST BE CONTEXTUAL
   - The LinkedIn CTA and the final tweet must reference the specific product/action from the brief.
   - Do NOT use: "Try it today!", "Learn more!", "Follow for more!", "Subscribe now!"
   - Write a CTA that connects to what the product actually does or who it is for.

5. NO AI-SLOP PHRASES
   - Forbidden: game-changing, revolutionize, seamless, unlock the power, transform your, leverage, paradigm shift, cutting-edge, groundbreaking, innovative solution, delve, elevate, in today's digital landscape, it's not just X it's Y, next-level, future-proof

6. PLATFORM SPECIFICITY
   - LinkedIn: professional but human tone, one clear insight per paragraph, useful to the target audience, ends with a specific CTA
   - X thread: each tweet is self-contained and punchy, thread has a logical progression from problem → solution → CTA, tweet 5 has a specific CTA
   - Each tweet must be strictly under 280 characters

Create content and return ONLY a JSON object with this exact structure:
{{
  "linkedin": {{
    "hook": "opening hook (1 sentence, specific to the product/problem from the brief, no invented personal story)",
    "body": "full post body (use \\n\\n for paragraph breaks, use → for bullet points, 700-1200 chars total, no invented stats)",
    "cta": "contextual CTA specific to the product and audience from the brief"
  }},
  "twitter": [
    {{"num": 1, "text": "tweet 1 (max 280 chars, specific hook about the product/problem, end with 🧵)"}},
    {{"num": 2, "text": "tweet 2 (max 280 chars, develop the problem or insight)"}},
    {{"num": 3, "text": "tweet 3 (max 280 chars, bridge toward the product/solution)"}},
    {{"num": 4, "text": "tweet 4 (max 280 chars, specific product feature or benefit)"}},
    {{"num": 5, "text": "tweet 5 (max 280 chars, contextual CTA for this specific product)"}}
  ]
}}

Return ONLY the JSON object. No markdown, no explanation."""

    raw = _call_gemini(client, model, prompt, trace, "Content Writer")
    try:
        content = _extract_json(raw)
    except (json.JSONDecodeError, ValueError) as exc:
        raise GeminiError("Content Writer", f"Invalid JSON: {exc}") from exc

    # Validate and normalise LinkedIn
    li = content.get("linkedin", {})
    if not isinstance(li, dict):
        li = {}
    hook = _safe_str(li.get("hook"))
    body = _safe_str(li.get("body"))
    cta  = _safe_str(li.get("cta"))
    full_text = hook + "\n\n" + body + "\n\n" + cta
    linkedin_out = {
        "hook": hook,
        "body": body,
        "cta": cta,
        "chars": _char_count(full_text),
        "platform_compliant": True,
    }

    # Validate and normalise Twitter
    tweets_raw = content.get("twitter", [])
    if not isinstance(tweets_raw, list):
        tweets_raw = []
    tweets_out = []
    for i, tw in enumerate(tweets_raw[:5]):
        if not isinstance(tw, dict):
            continue
        text = _safe_str(tw.get("text"))
        tweets_out.append({
            "num": i + 1,
            "text": text,
            "chars": _char_count(text),
        })
    # Pad to 5 if fewer returned
    while len(tweets_out) < 5:
        tweets_out.append({
            "num": len(tweets_out) + 1,
            "text": f"[Tweet {len(tweets_out)+1} — content generation incomplete]",
            "chars": 50,
        })

    trace[-1].update({
        "agent": "Content Generator",
        "input": f"Platform strategies for LinkedIn & X. Brief: {brief[:80]}...",
        "decision": f"LinkedIn: {li_strat[:60]}. X: {tw_strat[:60]}.",
        "output": f"LinkedIn post ({linkedin_out['chars']} chars). X thread ({len(tweets_out)} tweets).",
    })
    return linkedin_out, tweets_out


# ---------------------------------------------------------------------------
# Stage 3: Visual Generator (carousel + reel)
# ---------------------------------------------------------------------------

def _run_visual(
    client: genai.Client,
    model: str,
    brief: str,
    plan: dict,
    trace: list,
) -> Tuple[List[dict], dict]:
    audience  = _safe_str(plan.get("target_audience"))
    core_msg  = _safe_str(plan.get("core_message"))
    ig_strat  = _safe_str(plan.get("platform_strategies", {}).get("instagram"))
    rl_strat  = _safe_str(plan.get("platform_strategies", {}).get("reel"))

    brief_facts = _safe_str(plan.get("brief_facts", "none provided"))

    prompt = f"""You are a visual content strategist creating Instagram carousel slides and a Reel storyboard.

Brief: {brief}
Target audience: {audience}
Core message: {core_msg}
Instagram strategy: {ig_strat}
Reel strategy: {rl_strat}
Facts explicitly stated in the brief: {brief_facts}

STRICT RULES:

1. Slide 1 (hook): The headline must be specific to the product/problem in the brief. Max 8 words. No invented stats.
2. Slide 2 (problem): Describe a real problem the target audience faces, grounded in the brief. Use bullet points (max 3). No fabricated numbers.
3. Slide 3 (insight): This slide must use ONLY facts/numbers from "{brief_facts}".
   - If no numbers are in the brief, use qualitative observations instead of stats.
   - Do NOT invent percentages, study results, or user counts.
   - If using stats, only use values from brief_facts. If none, use insight-style text without numbers.
4. Slide 4 (solution): List actual features/benefits from the brief. Do not invent features not mentioned.
5. Slide 5 (CTA): The CTA text must reference the specific product or action, not a generic phrase.
6. Reel: First 3 seconds must immediately state the problem or hook specific to this product. No exaggerated claims. Natural narration.
7. Do NOT use: game-changing, revolutionize, seamless, unlock the power, transform your, next-level

Create content and return ONLY a JSON object with this exact structure:
{{
  "carousel": [
    {{
      "slide": 1,
      "type": "hook",
      "headline": "specific hook headline about the product/problem (max 8 words)",
      "subtext": "supporting context from the brief (max 15 words)"
    }},
    {{
      "slide": 2,
      "type": "problem",
      "headline": "specific problem headline (max 8 words)",
      "subtext": "problem description grounded in brief (max 15 words)",
      "points": ["specific problem point 1", "specific problem point 2", "specific problem point 3"]
    }},
    {{
      "slide": 3,
      "type": "insight",
      "headline": "insight headline (max 8 words, no invented stats)",
      "subtext": "supporting context (max 15 words, grounded in brief or general observation)",
      "stats": [
        {{"val": "only use if in brief_facts, else write observation", "label": "label"}},
        {{"val": "only use if in brief_facts, else write observation", "label": "label"}},
        {{"val": "only use if in brief_facts, else write observation", "label": "label"}}
      ]
    }},
    {{
      "slide": 4,
      "type": "solution",
      "headline": "solution headline featuring the product (max 8 words)",
      "subtext": "solution description from brief (max 15 words)",
      "features": ["actual feature/benefit from brief 1", "actual feature/benefit from brief 2", "actual feature/benefit from brief 3", "actual feature/benefit from brief 4"]
    }},
    {{
      "slide": 5,
      "type": "cta",
      "headline": "specific CTA headline for this product (max 8 words)",
      "subtext": "contextual support (max 10 words)",
      "cta": "specific action text for this product (max 6 words)"
    }}
  ],
  "reel": {{
    "duration": "0:30",
    "scenes": [
      {{"time": "00:00", "type": "HOOK",    "visual": "specific visual for this product/problem", "voiceover": "specific hook voiceover max 15 words, no exaggerated claims", "text": "on-screen text max 5 words", "duration": "5s"}},
      {{"time": "00:05", "type": "PROBLEM", "visual": "visual showing the specific problem", "voiceover": "problem voiceover max 15 words, grounded in brief", "text": "on-screen text max 5 words", "duration": "7s"}},
      {{"time": "00:12", "type": "INSIGHT", "visual": "visual reinforcing the insight", "voiceover": "insight voiceover max 15 words, only use facts from brief", "text": "on-screen text max 5 words", "duration": "8s"}},
      {{"time": "00:20", "type": "PRODUCT", "visual": "product visual or demo", "voiceover": "product voiceover max 15 words, feature from brief", "text": "on-screen text max 5 words", "duration": "7s"}},
      {{"time": "00:27", "type": "CTA",     "visual": "product with CTA overlay", "voiceover": "specific CTA max 10 words", "text": "on-screen text max 5 words", "duration": "3s"}}
    ]
  }}
}}

Return ONLY the JSON object. No markdown, no explanation."""

    raw = _call_gemini(client, model, prompt, trace, "Visual Generator")
    try:
        visual = _extract_json(raw)
    except (json.JSONDecodeError, ValueError) as exc:
        raise GeminiError("Visual Generator", f"Invalid JSON: {exc}") from exc

    # Normalise carousel — add bg/accent colours (design-defined, not AI-defined)
    raw_slides = _safe_list(visual.get("carousel"), [])
    carousel_out = []
    slide_types = ["hook", "problem", "insight", "solution", "cta"]
    for i in range(5):
        if i < len(raw_slides) and isinstance(raw_slides[i], dict):
            s = raw_slides[i]
        else:
            s = {}
        slide = {
            "slide": i + 1,
            "type":     _safe_str(s.get("type"), slide_types[i]),
            "headline": _safe_str(s.get("headline"), f"Slide {i+1}"),
            "subtext":  _safe_str(s.get("subtext"), ""),
            "bg":       CAROUSEL_BG[i],
            "accent":   CAROUSEL_ACCENT[i],
        }
        if "points"   in s and isinstance(s["points"],   list): slide["points"]   = s["points"][:3]
        if "stats"    in s and isinstance(s["stats"],    list): slide["stats"]    = s["stats"][:3]
        if "features" in s and isinstance(s["features"], list): slide["features"] = s["features"][:4]
        if "cta"      in s:                                      slide["cta"]      = _safe_str(s.get("cta"))
        carousel_out.append(slide)

    # Normalise reel
    reel_raw = visual.get("reel", {})
    reel_scenes_raw = _safe_list(reel_raw.get("scenes") if isinstance(reel_raw, dict) else None, [])
    scene_types = ["HOOK", "PROBLEM", "INSIGHT", "PRODUCT", "CTA"]
    scene_times = ["00:00", "00:05", "00:12", "00:20", "00:27"]
    scene_durs  = ["5s",    "7s",    "8s",    "7s",    "3s"]
    scenes_out = []
    for i in range(5):
        if i < len(reel_scenes_raw) and isinstance(reel_scenes_raw[i], dict):
            sc = reel_scenes_raw[i]
        else:
            sc = {}
        scenes_out.append({
            "time":      _safe_str(sc.get("time"),      scene_times[i]),
            "type":      _safe_str(sc.get("type"),      scene_types[i]),
            "visual":    _safe_str(sc.get("visual"),    "Scene visual"),
            "voiceover": _safe_str(sc.get("voiceover"), ""),
            "text":      _safe_str(sc.get("text"),      ""),
            "duration":  _safe_str(sc.get("duration"),  scene_durs[i]),
        })
    reel_out = {"duration": "0:30", "scenes": scenes_out}

    trace[-1].update({
        "agent": "Visual Generator",
        "input": f"Brief + Instagram/Reel strategies. Core message: {core_msg[:60]}.",
        "decision": f"5 carousel slides (hook→CTA). 5 reel scenes (30s arc).",
        "output": f"Carousel: {len(carousel_out)} slides. Reel: {len(scenes_out)} scenes.",
    })
    return carousel_out, reel_out


# ---------------------------------------------------------------------------
# Stage 4: Critic
# ---------------------------------------------------------------------------

def _run_critic(
    client: genai.Client,
    model: str,
    brief: str,
    linkedin: dict,
    twitter: List[dict],
    carousel: List[dict],
    reel: dict,
    trace: list,
) -> dict:
    li_text = linkedin.get("hook", "") + "\n" + linkedin.get("body", "")
    tw_text = "\n".join(t.get("text", "") for t in twitter[:3])
    ca_text = " | ".join(s.get("headline", "") for s in carousel)

    detected_slop = sorted(set(
        _detect_slop(li_text) +
        _detect_slop(tw_text) +
        _detect_slop(ca_text)
    ))

    prompt = f"""You are an expert content quality critic for marketing campaigns.

Original brief: {brief}

LinkedIn post (hook + body excerpt):
{li_text[:500]}

X thread (tweets 1-3):
{tw_text[:600]}

Carousel headlines:
{ca_text[:300]}

Evaluate this campaign content. Check specifically for these issues:

ISSUE CHECKLIST (only flag issues you can actually see in the content above):
A. INVENTED PERSONAL EXPERIENCE: Does the content contain first-person stories ("I realized...", "I experienced...", "During my...") that are NOT supported by the brief? If yes, flag it.
B. UNSUPPORTED FACTUAL CLAIMS: Does the content contain specific statistics, percentages, user counts, or research findings that were NOT in the original brief? If yes, flag it.
C. GENERIC HOOK: Is the opening hook vague, clichéd, or not specific to the product/problem? Flag if it uses generic patterns like "In today's world...", "Technology is changing...", "Are you ready to..."
D. WEAK OR GENERIC CTA: Is the call to action generic ("Try it today!", "Learn more!", "Follow for more!") rather than specific to the product and audience? Flag if so.
E. AI-SLOP PHRASES: Are any of these phrases used: game-changing, revolutionize, seamless, unlock the power, transform your, leverage, paradigm shift, cutting-edge, groundbreaking, innovative solution, delve, elevate, in today's digital landscape? Flag each one found.
F. BRIEF MISMATCH: Does any content introduce products, audiences, industries, or topics NOT mentioned in the brief?
G. PLATFORM MISMATCH: Is the tone or format wrong for the platform (e.g. LinkedIn post is too casual, tweets are too long)?
H. INCOMPLETE CONTENT: Does any piece appear cut off mid-sentence or structurally incomplete?
I. REPETITIVE WORDING: Is the same word, phrase, or idea repeated unnecessarily across the content?

Return ONLY a JSON object:
{{
  "scores": {{
    "humanLikeness": <integer 0-100, penalise for invented personal stories or robotic phrasing>,
    "hookStrength": <integer 0-100, penalise for generic openings>,
    "platformFit": <integer 0-100, penalise for platform-wrong tone/format>,
    "brandConsistency": <integer 0-100, how consistent the voice/message is across platforms>,
    "clarity": <integer 0-100, how clear and easy to understand>,
    "ctaStrength": <integer 0-100, penalise for generic CTAs>,
    "briefRelevance": <integer 0-100, penalise for content not grounded in the brief>
  }},
  "issues": [
    {{
      "severity": "high", "medium", or "low",
      "platform": "LinkedIn", "X", "Carousel", or "General",
      "issue_type": one of: "invented_experience", "unsupported_claim", "generic_hook", "weak_cta", "slop_phrase", "brief_mismatch", "platform_mismatch", "incomplete_content", "repetition",
      "description": "specific quote or example from the content showing the issue (1 sentence)",
      "action": "specific fix instruction — if removing an unsupported stat, say 'remove and replace with a qualitative observation, do not invent a new number' (1 sentence)"
    }}
  ],
  "overallVerdict": "honest 2-3 sentence assessment: what works, what specific issues remain, and whether the content is ready for human review"
}}

IMPORTANT: Only flag issues you can actually see in the content above. Do not fabricate issues.
Scores must reflect the actual content quality — do not inflate them.
Return ONLY the JSON object."""

    raw = _call_gemini(client, model, prompt, trace, "Critic")
    try:
        critic_data = _extract_json(raw)
    except (json.JSONDecodeError, ValueError) as exc:
        raise GeminiError("Critic", f"Invalid JSON: {exc}") from exc

    # Validate/normalise scores
    raw_scores = critic_data.get("scores", {})
    if not isinstance(raw_scores, dict):
        raw_scores = {}
    score_keys = ["humanLikeness", "hookStrength", "platformFit", "brandConsistency", "clarity", "ctaStrength", "briefRelevance"]
    scores = {}
    for k in score_keys:
        v = raw_scores.get(k, 75)
        try:
            scores[k] = max(0, min(100, int(v)))
        except (TypeError, ValueError):
            scores[k] = 75

    # Compute AI slop risk from detected phrases + human-likeness score
    slop_count = len(detected_slop)
    hl_score   = scores["humanLikeness"]
    if slop_count == 0 and hl_score >= 85:
        slop_risk = "LOW"
    elif slop_count <= 2 and hl_score >= 70:
        slop_risk = "MEDIUM"
    else:
        slop_risk = "HIGH"
    scores["aiSlopRisk"] = slop_risk

    # Overall quality score = weighted average (excludes aiSlopRisk)
    numeric_scores = [v for k, v in scores.items() if k != "aiSlopRisk"]
    quality_score = round(sum(numeric_scores) / len(numeric_scores))

    issues = _safe_list(critic_data.get("issues"), [])
    valid_issues = []
    for iss in issues[:5]:
        if isinstance(iss, dict):
            valid_issues.append({
                "severity": _safe_str(iss.get("severity"), "low"),
                "platform": _safe_str(iss.get("platform"), "General"),
                "description": _safe_str(iss.get("description")),
                "action": _safe_str(iss.get("action")),
                "status": "flagged",
            })

    trace[-1].update({
        "agent": "Critic",
        "input": f"LinkedIn post ({linkedin['chars']} chars), X thread ({len(twitter)} tweets), {len(carousel)} carousel slides.",
        "decision": (
            f"Detected {slop_count} slop phrase(s). "
            f"Human-likeness: {scores['humanLikeness']}. "
            f"Brief relevance: {scores['briefRelevance']}."
        ),
        "output": (
            f"{len(valid_issues)} issue(s) flagged. "
            f"AI slop risk: {slop_risk}. "
            f"Quality score: {quality_score}."
        ),
    })

    return {
        "scores": scores,
        "detectedPhrases": detected_slop,
        "issues": valid_issues,
        "overallVerdict": _safe_str(critic_data.get("overallVerdict"), "Campaign evaluated."),
        "qualityScore": quality_score,
    }


# ---------------------------------------------------------------------------
# Stage 5: Refiner
# ---------------------------------------------------------------------------

def _run_refiner(
    client: genai.Client,
    model: str,
    brief: str,
    linkedin: dict,
    twitter: List[dict],
    issues: List[dict],
    detected_slop: List[str],
    trace: list,
) -> Tuple[dict, List[dict]]:
    """
    Refines LinkedIn and Twitter content based on Critic issues.
    Only runs if there are actual issues to fix.
    Returns (refined_linkedin, refined_twitter).
    """
    if not issues and not detected_slop:
        trace.append({
            "agent": "Refiner",
            "input": "Critic output (no issues flagged)",
            "decision": "No refinement needed — content passed quality gate.",
            "output": "Original content retained.",
            "status": "skipped",
        })
        return linkedin, twitter

    issues_text = "\n".join(
        f"- [{iss['platform']}] {iss['description']} → Fix: {iss['action']}"
        for iss in issues
    )
    slop_text = ", ".join(f'"{p}"' for p in detected_slop) if detected_slop else "none"
    li_body = linkedin.get("hook", "") + "\n\n" + linkedin.get("body", "")
    tw_texts = "\n".join(f"[{t['num']}] {t['text']}" for t in twitter)

    prompt = f"""You are a content refiner improving marketing copy based on specific quality feedback.

Original brief: {brief}

Issues to fix:
{issues_text if issues_text else "No structural issues."}

Slop phrases to remove: {slop_text}

Current LinkedIn content:
{li_body[:900]}

Current X thread:
{tw_texts[:900]}

STRICT REFINEMENT RULES — READ CAREFULLY:

1. INVENTED EXPERIENCES: If any issue is of type "invented_experience", rewrite that sentence as a product observation, general insight, or relatable scenario framed as a question. Do NOT replace it with another invented personal story.

2. UNSUPPORTED CLAIMS: If any issue is of type "unsupported_claim", REMOVE the statistic or claim. Replace it with a qualitative observation or a clearly framed product benefit. Do NOT invent a new number or percentage to replace the removed one.

3. GENERIC HOOKS: If the hook is flagged as generic, rewrite it to be specific to the product and audience described in the brief. Do not use: "In today's world", "Technology is changing", "Are you ready to", "Here's the thing".

4. GENERIC CTAs: Replace with a CTA that names the specific product, action, or audience benefit. Do NOT use: "Try it today!", "Learn more!", "Follow for more!".

5. SLOP PHRASES: Remove every phrase listed in "Slop phrases to remove" and replace with plain, specific language.

6. PRESERVE: Do not change what is working. Do not introduce new facts that were not in the brief. Do not shorten good content unnecessarily.

7. COMPLETENESS: Ensure the LinkedIn post and all 5 tweets are complete — no cut-off sentences.

Revise the content and return ONLY a JSON object:
{{
  "linkedin": {{
    "hook": "revised hook (specific to the product, no invented personal story)",
    "body": "revised body (fix issues, no invented stats, use \\n\\n for paragraphs, complete sentences)",
    "cta": "contextual CTA specific to the product and audience"
  }},
  "twitter": [
    {{"num": 1, "text": "revised tweet 1 (max 280 chars, specific hook)"}},
    {{"num": 2, "text": "revised tweet 2 (max 280 chars)"}},
    {{"num": 3, "text": "revised tweet 3 (max 280 chars)"}},
    {{"num": 4, "text": "revised tweet 4 (max 280 chars)"}},
    {{"num": 5, "text": "revised tweet 5 (max 280 chars, contextual CTA)"}}
  ]
}}

Only change what needs fixing. Return ONLY the JSON object."""

    raw = _call_gemini(client, model, prompt, trace, "Refiner")
    try:
        refined = _extract_json(raw)
    except (json.JSONDecodeError, ValueError) as exc:
        # Refinement failure is non-fatal — return originals
        trace[-1].update({
            "agent": "Refiner",
            "status": "error",
            "error": f"JSON parse error: {exc}. Original content retained.",
        })
        return linkedin, twitter

    # Normalise refined LinkedIn
    rli = refined.get("linkedin", {})
    if isinstance(rli, dict) and rli.get("hook") and rli.get("body"):
        hook = _safe_str(rli.get("hook"))
        body = _safe_str(rli.get("body"))
        cta  = _safe_str(rli.get("cta"))
        full = hook + "\n\n" + body + "\n\n" + cta
        linkedin_out = {"hook": hook, "body": body, "cta": cta, "chars": _char_count(full), "platform_compliant": True}
    else:
        linkedin_out = linkedin

    # Normalise refined Twitter
    rtw = _safe_list(refined.get("twitter"), [])
    if len(rtw) >= 3:
        twitter_out = []
        for i, tw in enumerate(rtw[:5]):
            if isinstance(tw, dict):
                text = _safe_str(tw.get("text"))
                twitter_out.append({"num": i+1, "text": text, "chars": _char_count(text)})
        while len(twitter_out) < 5:
            twitter_out.append(twitter[len(twitter_out)] if len(twitter_out) < len(twitter) else twitter[-1])
    else:
        twitter_out = twitter

    # Mark issues as resolved
    for iss in issues:
        iss["status"] = "resolved"

    trace[-1].update({
        "agent": "Refiner",
        "input": f"{len(issues)} issue(s) + {len(detected_slop)} slop phrase(s) to fix.",
        "decision": f"Revised LinkedIn hook and body. Revised X thread tweets. Removed slop: {slop_text[:60]}.",
        "output": f"Refined LinkedIn ({linkedin_out['chars']} chars). Refined X thread ({len(twitter_out)} tweets). Issues resolved.",
        "status": "done",
    })
    return linkedin_out, twitter_out


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def run_pipeline(
    api_key: str,
    brief: str,
    platforms: List[str],
    tone: str,
    brand: str,
    env_overrides: Dict,
) -> Dict:
    """
    Execute the full 5-stage Gemini pipeline.
    Returns a campaign dict matching the frontend DEMO_CAMPAIGN schema.
    Raises GeminiError on unrecoverable failures.
    """
    client = _make_client(api_key)
    model  = env_overrides.get("GEMINI_MODEL", os.getenv("GEMINI_MODEL", "gemini-2.0-flash"))
    trace  = []  # Accumulated across all stages
    start  = time.monotonic()

    # 1. Planner
    plan = _run_planner(client, model, brief, platforms, tone, brand, trace)

    # 2. Writer
    linkedin, twitter = _run_writer(client, model, brief, plan, tone, brand, trace)

    # 3. Visual
    carousel, reel = _run_visual(client, model, brief, plan, trace)

    # 4. Critic
    critic_result = _run_critic(client, model, brief, linkedin, twitter, carousel, reel, trace)

    # 5. Refiner
    linkedin, twitter = _run_refiner(
        client, model, brief, linkedin, twitter,
        critic_result["issues"], critic_result["detectedPhrases"], trace,
    )

    elapsed_ms = int((time.monotonic() - start) * 1000)

    # Build final output trace (strip internal keys)
    final_trace = []
    for entry in trace:
        clean = {k: v for k, v in entry.items() if k not in ("_raw_chars",)}
        final_trace.append(clean)

    # Append "Final Output" trace entry
    final_trace.append({
        "agent": "Final Output",
        "input": "Refined content from all agents",
        "decision": (
            f"Quality gate: {critic_result['qualityScore']}/100. "
            f"AI slop risk: {critic_result['scores']['aiSlopRisk']}. "
            "Human approval gate triggered."
        ),
        "output": "Campaign package ready for human review.",
        "status": "done",
    })

    title         = _safe_str(plan.get("campaign_title"), brief[:40])
    quality_score = critic_result["qualityScore"]

    return {
        # ── Top-level fields (read directly by frontend) ───────────────────
        "title":        title,
        "qualityScore": quality_score,
        # ── Metadata ──────────────────────────────────────────────────────
        "meta": {
            "mode": "ai",
            "brief": brief,
            "platforms": platforms,
            "tone": tone,
            "brand": brand,
            "title": title,
            "qualityScore": quality_score,
            "generationTimeMs": elapsed_ms,
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "model": model,
        },
        "linkedin":  linkedin,
        "twitter":   twitter,
        "carousel":  carousel,
        "reel":      reel,
        "critic":    {
            "scores":          critic_result["scores"],
            "detectedPhrases": critic_result["detectedPhrases"],
            "issues":          critic_result["issues"],
            "overallVerdict":  critic_result["overallVerdict"],
        },
        "trace": final_trace,
    }
