from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class JobDescription:
    role: str
    experience_required: str
    mandatory_skills: List[str]
    supporting_skills: List[str]
    tools: List[str]
    domain_knowledge: List[str]
    responsibilities: List[str]


@dataclass
class Resume:
    candidate_name: str
    total_experience_years: float
    skills_with_context: List[Dict[str, Any]]
    projects: List[Dict[str, Any]]


@dataclass
class EvaluationResult:
    final_score: float
    category_scores: Dict[str, float]
    category_explanations: Dict[str, str]
