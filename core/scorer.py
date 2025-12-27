import json
import copy
from typing import Dict, Any

from core.llm_client import call_llm
from core.rubric import RUBRIC_CATEGORIES, get_rubric_text


LLM_OUTPUT_SCHEMA = {
    "Professional Presence": {
        "score": "number (0-100)",
        "explanation": "string"
    },
    "Experience & Seniority": {
        "score": "number (0-100)",
        "explanation": "string"
    },
    "Impact & Results": {
        "score": "number (0-100)",
        "explanation": "string"
    },
    "Skills Credibility & Domain Knowledge": {
        "score": "number (0-100)",
        "explanation": "string"
    },
    "Tools & Technology": {
        "score": "number (0-100)",
        "explanation": "string"
    },
    "Projects & Ownership": {
        "score": "number (0-100)",
        "explanation": "string"
    },
    "Resume Quality": {
        "score": "number (0-100)",
        "explanation": "string"
    }
}


# -------------------- SAFETY HELPERS --------------------

def mask_resume_pii(parsed_resume: Dict[str, Any]) -> Dict[str, Any]:
    """
    Removes personal identifiers before scoring.
    """
    resume = copy.deepcopy(parsed_resume)

    resume.pop("candidate_name", None)
    resume.pop("email", None)
    resume.pop("phone", None)
    resume.pop("professional_presence_links", None)

    return resume


def _extract_json(text: str) -> str:
    if not text:
        return ""

    text = text.strip()
    if text.startswith("```"):
        parts = text.split("```")
        if len(parts) >= 2:
            text = parts[1]

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        text = text[start:end + 1]

    return text.strip()


def _safe_json_load(response_text: str) -> dict:
    try:
        cleaned = _extract_json(response_text)
        return json.loads(cleaned)
    except Exception as exc:
        raise ValueError("Invalid JSON returned by LLM") from exc


def _validate_llm_scores(llm_scores: Dict[str, Any]) -> None:
    for category in RUBRIC_CATEGORIES:
        if category not in llm_scores:
            raise ValueError(f"Missing category: {category}")

        score = llm_scores[category].get("score")
        if not isinstance(score, (int, float)):
            raise ValueError(f"Invalid score type for {category}")

        if score < 0 or score > 100:
            raise ValueError(f"Score out of range for {category}")


def _compute_final_score(llm_scores: Dict[str, Any]) -> float:
    final_score = 0.0
    for category, weight in RUBRIC_CATEGORIES.items():
        final_score += llm_scores[category]["score"] * (weight / 100)
    return round(final_score, 2)


def assign_candidate_tier(final_score: float) -> str:
    if final_score >= 80:
        return "TOP"
    elif final_score >= 60:
        return "BEST"
    elif final_score >= 40:
        return "MODERATE"
    elif final_score >= 20:
        return "LOW"
    else:
        return "VERY_LOW"


# -------------------- PROMPT --------------------

def _build_prompt(parsed_jd: Dict[str, Any], parsed_resume: Dict[str, Any]) -> str:
    return f"""
{get_rubric_text()}

SCORING INTELLIGENCE RULES (MANDATORY):

1. Perform SEMANTIC matching, not keyword matching
   - Example: "MongoDB" ≈ "MongoDB Compass"
   - Example: "Python" ≈ "Python frameworks"

2. WEIGHT USAGE OVER MENTION
   - Skill/tool used in projects or experience = higher score
   - Mentioned only in skills list = lower score

3. LOCATION LOGIC (Professional Presence)
   - If JD location exists AND resume location matches → positive signal
   - If JD location exists AND resume location missing → neutral
   - If JD location is null → ignore location completely

4. DO NOT penalize missing optional fields
5. Do NOT infer experience or skills
6. Compare JD and Resume contextually, not literally
7. Do NOT compute final score

STRICT OUTPUT RULES:
- Output MUST be valid JSON
- Follow EXACT schema
- Scores must be 0–100
- Explanations must justify semantic reasoning

REQUIRED JSON SCHEMA:
{json.dumps(LLM_OUTPUT_SCHEMA, indent=2)}

PARSED JOB DESCRIPTION:
{json.dumps(parsed_jd, indent=2)}

PARSED RESUME (PII MASKED):
{json.dumps(parsed_resume, indent=2)}

Return ONLY valid JSON.
"""


# -------------------- MAIN ENTRY --------------------

def score_resume(parsed_jd: Dict[str, Any], parsed_resume: Dict[str, Any]) -> Dict[str, Any]:
    masked_resume = mask_resume_pii(parsed_resume)

    prompt = _build_prompt(parsed_jd, masked_resume)
    response = call_llm(prompt)

    try:
        llm_scores = _safe_json_load(response)
        _validate_llm_scores(llm_scores)
    except Exception:
        retry_prompt = prompt + "\nERROR: Fix JSON. Return ONLY JSON."
        retry_response = call_llm(retry_prompt)
        llm_scores = _safe_json_load(retry_response)
        _validate_llm_scores(llm_scores)

    final_score = _compute_final_score(llm_scores)
    candidate_tier = assign_candidate_tier(final_score)

    return {
        "final_score": final_score,
        "candidate_tier": candidate_tier,
        "category_scores": {
            cat: llm_scores[cat]["score"] for cat in RUBRIC_CATEGORIES
        },
        "category_explanations": {
            cat: llm_scores[cat]["explanation"] for cat in RUBRIC_CATEGORIES
        }
    }
