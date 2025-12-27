import os
import json
from groq import Groq
from core.config_manager import ConfigManager

_client = Groq(api_key=ConfigManager.get("GROQ_API_KEY"))


# ------------------ CHAT COMPLETION ------------------ #

def call_llm(prompt: str) -> str:
    response = _client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


# ------------------ EMBEDDING VIA LLM ------------------ #

def call_llm_embedding(text: str) -> list[float]:
    """
    Generates a semantic embedding vector using Groq free LLM.
    This is NOT scoring, only meaning representation.
    """

    embedding_prompt = f"""
You are a semantic embedding generator.
s
TASK:
Convert the following text into a numerical vector that captures its semantic meaning.

RULES:
- Output ONLY valid JSON
- Output must be a list of EXACTLY 128 floating point numbers
- Numbers must be between -1 and 1
- Same input text must produce similar vectors
- No explanation, no markdown

TEXT:
\"\"\"
{text}
\"\"\"

Return ONLY the JSON array.
"""

    response = _client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": embedding_prompt}],
        temperature=0,
    )

    raw = response.choices[0].message.content.strip()

    try:
        vector = json.loads(_extract_json(raw))
        if not isinstance(vector, list) or len(vector) != 128:
            raise ValueError("Invalid embedding size")
        return vector
    except Exception as exc:
        raise RuntimeError("Failed to generate embedding") from exc


def _extract_json(text: str) -> str:
    text = text.strip()
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1:
        return text[start:end + 1]
    return ""
