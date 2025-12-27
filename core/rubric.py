"""
Static, human-defined evaluation rubric.

This module MUST NOT contain any LLM logic.
It defines the categories, weights, and instructions
that the LLM must follow strictly.
"""

RUBRIC_CATEGORIES = {
    "Professional Presence": 5,
    "Experience & Seniority": 20,
    "Impact & Results": 10,
    "Skills Credibility & Domain Knowledge": 25,
    "Tools & Technology": 20,
    "Projects & Ownership": 15,
    "Resume Quality": 5
}

TOTAL_WEIGHT = sum(RUBRIC_CATEGORIES.values())


def get_rubric_text() -> str:
    """
    Returns rubric instructions to be sent to the LLM.
    """
    return """
You are a resume evaluation engine.

You MUST evaluate the resume strictly using the following categories.
Do NOT add, remove, rename, or merge categories.
Do NOT change weights.
Do NOT compute the final score.

CATEGORIES (Score each from 0 to 100):
1. Professional Presence
2. Experience & Seniority
3. Impact & Results
4. Skills Credibility & Domain Knowledge
5. Tools & Technology
6. Projects & Ownership
7. Resume Quality

For EACH category:
- Assign a numeric score between 0 and 100
- Provide a short explanation (1–2 sentences)

Return ONLY valid JSON in the required schema.
"""
