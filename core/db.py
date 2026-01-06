import os
from datetime import datetime
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


# =====================
# DASHBOARD & STATS
# =====================
def get_jd_by_title(role: str, org_id: str = None):
    """
    Check if a JD with the same role/title already exists for the organization.
    Returns the JD document if found, None otherwise.
    Checks both 'role' and 'job_title' fields.
    """
    query = {"$or": [{"role": role}, {"job_title": role}]}
    if org_id:
        query["org_id"] = org_id
    return _db.jds.find_one(query, {"_id": 0})


def get_total_resumes_count(org_id: str = None):
    """
    Get total number of resumes for an organization.
    """
    query = {}
    if org_id:
        query["org_id"] = org_id
    return _db.resumes.count_documents(query)


def get_average_match_score(org_id: str = None):
    """
    Calculate average matching score across all evaluations for an organization.
    Returns 0 if no evaluations exist.
    """
    query = {}
    if org_id:
        query["org_id"] = org_id
    
    evaluations = list(_db.evaluations.find(query, {"overall_score": 1, "_id": 0}))
    
    if not evaluations:
        return 0.0
    
    total_score = sum(ev["overall_score"] for ev in evaluations)
    return round(total_score / len(evaluations), 1)


def get_job_stats(org_id: str = None):
    """
    Get comprehensive stats for dashboard including list of jobs with resume counts.
    Returns list of job stats with resume count for each.
    """
    jds = get_jds(org_id=org_id)
    
    job_stats = []
    for jd in jds:
        # Count resumes for this JD with org_id filter
        query = {"jd_id": jd["jd_id"]}
        if org_id:
            query["org_id"] = org_id
        resume_count = _db.resumes.count_documents(query)
        
        job_stats.append({
            "jd_id": jd["jd_id"],
            "role": jd.get("role", jd.get("job_title", "Unknown")),
            "created_at": jd.get("created_at"),
            "resume_count": resume_count
        })
    
    return job_stats


# =====================
# DELETE JOB & CASCADE
# =====================
def delete_job_and_related_data(jd_id: str, org_id: str = None):
    """
    Delete a job and all its related data (resumes, evaluations, file_fingerprints).
    This is a cascading delete operation.
    
    Returns: dict with success status and message
    """
    try:
        # Build query with org_id filter
        query = {"jd_id": jd_id}
        if org_id:
            query["org_id"] = org_id
        
        # Delete all evaluations for this job
        eval_result = _db.evaluations.delete_many(query)
        
        # Delete all resumes for this job
        resume_result = _db.resumes.delete_many(query)
        
        # Delete file_fingerprints if collection exists
        if "file_fingerprints" in _db.list_collection_names():
            _db.file_fingerprints.delete_many(query)
        
        # Delete the JD itself
        jd_query = {"jd_id": jd_id}
        if org_id:
            jd_query["org_id"] = org_id
        jd_result = _db.jds.delete_one(jd_query)
        
        if jd_result.deleted_count == 0:
            return {
                "success": False,
                "message": "Job not found or already deleted"
            }
        
        return {
            "success": True,
            "message": f"Job deleted successfully. Removed {resume_result.deleted_count} resumes and {eval_result.deleted_count} evaluations.",
            "deleted_resumes": resume_result.deleted_count,
            "deleted_evaluations": eval_result.deleted_count
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error deleting job: {str(e)}"
        }



# =====================
# FILE FINGERPRINTS - PREVENT DUPLICATE UPLOADS
# =====================
import hashlib

def compute_file_hash(file_content: bytes) -> str:
    """
    Compute SHA256 hash of file content.
    
    Args:
        file_content: Raw bytes of the file
        
    Returns:
        SHA256 hash string
    """
    return hashlib.sha256(file_content).hexdigest()


def check_jd_duplicate(file_hash: str, org_id: str = None) -> dict:
    """
    Check if a JD file has already been uploaded by this organization.
    
    Args:
        file_hash: SHA256 hash of the file
        org_id: Organization ID
        
    Returns:
        dict with 'is_duplicate' (bool) and 'existing_jd' (dict or None)
    """
    query = {
        "file_hash": file_hash,
        "file_type": "jd"
    }
    if org_id:
        query["org_id"] = org_id
    
    existing = _db.file_fingerprints.find_one(query)
    
    if existing:
        # Get the JD details
        jd = _db.jds.find_one({"jd_id": existing["jd_id"]}, {"_id": 0})
        return {
            "is_duplicate": True,
            "existing_jd": jd
        }
    
    return {
        "is_duplicate": False,
        "existing_jd": None
    }


def check_resume_duplicate(file_hash: str, jd_id: str, org_id: str = None) -> dict:
    """
    Check if a resume file has already been uploaded for this specific job.
    Same resume can be uploaded for different jobs.
    
    Args:
        file_hash: SHA256 hash of the file
        jd_id: Job ID to check against
        org_id: Organization ID
        
    Returns:
        dict with 'is_duplicate' (bool) and 'existing_resume' (dict or None)
    """
    query = {
        "file_hash": file_hash,
        "file_type": "resume",
        "jd_id": jd_id
    }
    if org_id:
        query["org_id"] = org_id
    
    existing = _db.file_fingerprints.find_one(query)
    
    if existing:
        # Get the resume details
        resume = _db.resumes.find_one({"resume_id": existing["resume_id"]}, {"_id": 0})
        return {
            "is_duplicate": True,
            "existing_resume": resume
        }
    
    return {
        "is_duplicate": False,
        "existing_resume": None
    }


def save_jd_fingerprint(file_hash: str, jd_id: str, filename: str, org_id: str = None):
    """
    Save JD file fingerprint to prevent duplicate uploads.
    
    Args:
        file_hash: SHA256 hash of the file
        jd_id: Job ID
        filename: Original filename
        org_id: Organization ID
    """
    doc = {
        "file_hash": file_hash,
        "file_type": "jd",
        "jd_id": jd_id,
        "filename": filename,
        "uploaded_at": datetime.utcnow()
    }
    if org_id:
        doc["org_id"] = org_id
    
    _db.file_fingerprints.insert_one(doc)


def save_resume_fingerprint(file_hash: str, resume_id: str, jd_id: str, filename: str, org_id: str = None):
    """
    Save resume file fingerprint to prevent duplicate uploads for the same job.
    
    Args:
        file_hash: SHA256 hash of the file
        resume_id: Resume ID
        jd_id: Job ID
        filename: Original filename
        org_id: Organization ID
    """
    doc = {
        "file_hash": file_hash,
        "file_type": "resume",
        "resume_id": resume_id,
        "jd_id": jd_id,
        "filename": filename,
        "uploaded_at": datetime.utcnow()
    }
    if org_id:
        doc["org_id"] = org_id
    
    _db.file_fingerprints.insert_one(doc)
