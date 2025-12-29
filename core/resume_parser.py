import json
from typing import Dict, Any

from core.llm_client import call_llm


RESUME_SCHEMA = {
    "candidate_name": "string or null",
    "total_experience_years": "number or null",
    "location": "string or null",
    "titles_with_dates": [
        {
            "title": "string",
            "organization": "string",
            "start_date": "string or null",
            "end_date": "string or null"
        }
    ],
    "career_progression": [
        "string"
    ],
    "skills_with_context": [
        {
            "skill": "string",
            "context": "string"
        }
    ],
    "tools_with_context": [
        {
            "tool": "string",
            "context": "string"
        }
    ],
    "domain_experience": [
        "string"
    ],
    "projects": [
        {
            "name": "string",
            "description": "string",
            "technologies": ["string"]
        }
    ],
    "leadership_signals": [
        "string"
    ],
    "impact_metrics": [
        "string"
    ],
    "professional_presence_links": [
        "string"
    ]
}


def _build_prompt(resume_text: str) -> str:
    """
    Builds a strict prompt to extract structured resume data.
    """
    return f"""
You are an enterprise resume parsing engine.

TASK:
Extract structured information from the resume text below.

STRICT RULES:
- Output MUST be valid JSON only
- Follow the EXACT schema provided
- Do NOT add explanations or comments
- Do NOT infer or assume missing information
- Do NOT score, rank, or evaluate
- Do NOT compare against any job description
- If information is missing, use null or empty lists
- Extract only what is explicitly stated in the resume

REQUIRED JSON SCHEMA:
{json.dumps(RESUME_SCHEMA, indent=2)}

RESUME TEXT:
\"\"\"
{resume_text}
\"\"\"

Return ONLY valid JSON.
"""


def _safe_json_load(response_text: str) -> Dict[str, Any]:
    """
    Safely loads JSON from LLM output.
    Raises ValueError if invalid.
    """
    
    try:
        cleaned = _extract_json(response_text)
        return json.loads(cleaned)
    except Exception as exc:
        raise ValueError("Invalid JSON returned by LLM") from exc


def parse_resume(resume_text: str) -> Dict[str, Any]:
    """
    Parses raw resume text into structured JSON.

    Flow:
    - Send resume text to Groq LLM
    - Validate JSON
    - Retry once if invalid
    - Fail fast if still invalid

    Args:
        resume_text (str): Raw resume text

    Returns:
        Dict[str, Any]: Structured resume JSON
    """

    prompt = _build_prompt(resume_text)

    # First attempt
    response = call_llm(prompt)

    try:
        return _safe_json_load(response)
    except ValueError:
        # Retry once with stronger instruction
        retry_prompt = prompt + "\n\nIMPORTANT: The previous output was invalid JSON. Fix it strictly."

        retry_response = call_llm(retry_prompt)

        try:
            return _safe_json_load(retry_response)
        except ValueError as exc:
            raise RuntimeError(
                "Groq LLM failed to return valid JSON after retry"
            ) from exc
def _extract_json(text: str) -> str:
    if not text:
        return ""

    text = text.strip()

    # Remove markdown fences if present
    if text.startswith("```"):
        parts = text.split("```")
        if len(parts) >= 2:
            text = parts[1]

    # Extract JSON boundaries
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        return ""

    return text[start:end + 1].strip()
