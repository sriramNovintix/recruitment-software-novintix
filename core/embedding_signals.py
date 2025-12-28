from typing import Dict, Any, List
import numpy as np

from core.embedding_client import embed_text  # wraps OpenAI / HF / etc


def _avg_embedding(texts: List[str]) -> List[float]:
    if not texts:
        return []
    vectors = [embed_text(t) for t in texts if t.strip()]
    return np.mean(vectors, axis=0).tolist() if vectors else []


def _cosine(a: List[float], b: List[float]) -> float:
    if not a or not b:
        return 0.0
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def compute_embedding_signals(
    jd: Dict[str, Any],
    resume: Dict[str, Any]
) -> Dict[str, float]:

    signals = {}

    # Skills
    jd_skills = jd.get("mandatory_skills", []) + jd.get("supporting_skills", [])
    res_skills = [s["skill"] for s in resume.get("skills_with_context", [])]

    signals["skills_similarity"] = round(
        _cosine(_avg_embedding(jd_skills), _avg_embedding(res_skills)) * 100, 2
    )

    # Tools
    signals["tools_similarity"] = round(
        _cosine(
            _avg_embedding(jd.get("tools", [])),
            _avg_embedding([t["tool"] for t in resume.get("tools_with_context", [])])
        ) * 100, 2
    )

    # Experience
    signals["experience_similarity"] = round(
        _cosine(
            _avg_embedding(jd.get("responsibilities", [])),
            _avg_embedding(resume.get("career_progression", []))
        ) * 100, 2
    )

    # Projects
    signals["project_similarity"] = round(
        _cosine(
            _avg_embedding(jd.get("responsibilities", [])),
            _avg_embedding([p["description"] for p in resume.get("projects", [])])
        ) * 100, 2
    )

    # Domain
    signals["domain_similarity"] = round(
        _cosine(
            _avg_embedding(jd.get("domain_knowledge", [])),
            _avg_embedding(resume.get("domain_experience", []))
        ) * 100, 2
    )

    return signals
