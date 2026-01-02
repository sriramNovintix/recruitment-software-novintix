import os
from pymongo import MongoClient, DESCENDING
from core.config_manager import ConfigManager

_client = None
_db = None


def init_db():
    global _client, _db

    uri = ConfigManager.get("MONGODB_URI")
    db_name = ConfigManager.get("DB_NAME")

    _client = MongoClient(uri)
    _db = _client[db_name]
    return _db


# =====================
# JD COLLECTION
# =====================
def save_jd(doc: dict, org_id: str = None):
    """
    Expects:
    {
        jd_id,
        role,
        parsed_jd_json,
        created_at,
        org_id (for multi-tenant support)
    }
    """
    if org_id:
        doc["org_id"] = org_id
    return _db.jds.insert_one(doc).inserted_id


def get_jds(org_id: str = None):
    query = {}
    if org_id:
        query["org_id"] = org_id
    return list(_db.jds.find(query, {"_id": 0}))


# =====================
# RESUME COLLECTION
# =====================
def save_resume(doc: dict, org_id: str = None):
    """
    Expects:
    {
        resume_id,
        candidate_name,
        jd_id,
        parsed_resume_json,
        created_at,
        org_id (for multi-tenant support)
    }
    """
    doc["status"] = "NOT_REVIEWED"
    if org_id:
        doc["org_id"] = org_id
    return _db.resumes.insert_one(doc).inserted_id

def get_unreviewed_resumes_by_jd(jd_id, org_id: str = None):
    query = {
        "jd_id": jd_id,
        "status": "NOT_REVIEWED"
    }
    if org_id:
        query["org_id"] = org_id
    return list(_db.resumes.find(query))

def mark_resume_reviewed(resume_id):
    _db.resumes.update_one(
        {"_id": resume_id},
        {"$set": {"status": "REVIEWED"}}
    )
def get_evaluations_by_jd_and_tier(jd_id, tier=None, limit=None, org_id: str = None):
    query = {"jd_id": jd_id}
    
    if org_id:
        query["org_id"] = org_id

    if tier and tier != "ALL":
        query["candidate_tier"] = tier

    cursor = _db.evaluations.find(query).sort("overall_score", -1)

    if limit:
        cursor = cursor.limit(limit)

    return list(cursor)


def get_resumes_by_jd(jd_id: str, org_id: str = None):
    query = {"jd_id": jd_id}
    if org_id:
        query["org_id"] = org_id
    return list(
        _db.resumes.find(query, {"_id": 0})
    )


# =====================
# EVALUATION COLLECTION
# =====================
def save_evaluation(doc: dict, org_id: str = None):
    """
    Expects:
    {
        evaluation_id,
        jd_id,
        resume_id,
        candidate_name,
        category_scores,
        overall_score,
        candidate_tier,
        evaluated_at,
        org_id (for multi-tenant support)
    }
    """
    if org_id:
        doc["org_id"] = org_id
    return _db.evaluations.insert_one(doc).inserted_id


def get_evaluations_by_jd(jd_id: str, limit: int = 10, org_id: str = None):
    """
    Returns ranked results for a JD
    """
    query = {"jd_id": jd_id}
    if org_id:
        query["org_id"] = org_id
    return list(
        _db.evaluations.find(query, {"_id": 0})
        .sort("overall_score", DESCENDING)
        .limit(limit)
    )

