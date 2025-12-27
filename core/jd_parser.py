import json
from typing import Dict, Any

from core.llm_client import call_llm


JD_SCHEMA = {
    "role": "string",
    "location": "string",
    "experience_required": "string or number (years)",
    "mandatory_skills": ["string"],
    "supporting_skills": ["string"],
    "tools": ["string"],
    "domain_knowledge": ["string"],
    "responsibilities": ["string"]
}


def _build_prompt(jd_text: str) -> str:
    """
    Builds a strict prompt to extract Job Description data
    without inference or scoring.
    """
    return f"""
You are an enterprise HR data extraction engine.

TASK:
Parse the following Job Description text and extract ONLY the information explicitly stated.

RULES (STRICT):
- Output MUST be valid JSON
- Output MUST follow the exact schema provided
- Do NOT add explanations
- Do NOT infer or assume missing information
- If a field is not clearly mentioned, return an empty list or null
- Do NOT score or rank anything
- Do NOT include candidate-related data

REQUIRED JSON SCHEMA:
{json.dumps(JD_SCHEMA, indent=2)}

JOB DESCRIPTION TEXT:
\"\"\"
{jd_text}
\"\"\"

Return ONLY valid JSON.
"""


def _safe_json_load(response_text: str) -> Dict[str, Any]:
    """
    Attempts to load JSON safely.
    Raises ValueError if invalid.
    """
    try:
        cleaned = _extract_json(response_text)
        return json.loads(cleaned)
    except Exception as exc:
        raise ValueError("Invalid JSON returned by LLM") from exc


def parse_jd(jd_text: str) -> Dict[str, Any]:
    """
    Parses raw Job Description text into a structured JSON format.

    Flow:
    - Send JD to Groq LLM
    - Validate JSON
    - Retry once if JSON is invalid
    - Raise error if still invalid

    Args:
        jd_text (str): Raw job description text

    Returns:
        Dict[str, Any]: Structured JD JSON
    """

    prompt = _build_prompt(jd_text)

    # First attempt
    response = call_llm(prompt)

    try:
        return _safe_json_load(response)
    except ValueError:
        # Retry once with reinforcement
        retry_prompt = prompt + "\n\nIMPORTANT: The previous output was invalid JSON. Fix it."

        retry_response = call_llm(retry_prompt)

        try:
            return _safe_json_load(retry_response)
        except ValueError as exc:
            raise RuntimeError(
                "Groq LLM failed to return valid JSON after retry"
            ) from exc

def _extract_json(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
    return text.strip()