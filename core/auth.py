"""
Authentication module for user/organization management
Each user is treated as an organization with multiple jobs
"""
import hashlib
import uuid
from datetime import datetime
from core.config_manager import ConfigManager
from pymongo import MongoClient

_client = None
_db = None


def get_auth_db():
    """Initialize or return existing database connection"""
    global _client, _db
    
    if _db is None:
        uri = ConfigManager.get("MONGODB_URI")
        db_name = ConfigManager.get("DB_NAME")
        _client = MongoClient(uri)
        _db = _client[db_name]
    
    return _db


def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(full_name: str, email: str, password: str, organization: str) -> dict:
    """
    Create a new user/organization
    Returns: {"success": bool, "message": str, "user_id": str or None}
    """
    db = get_auth_db()
    
    # Check if email already exists
    existing_user = db.users.find_one({"email": email.lower()})
    if existing_user:
        return {"success": False, "message": "Email already registered", "user_id": None}
    
    # Organization name can be reused - no uniqueness check
    
    user_id = str(uuid.uuid4())
    user_doc = {
        "user_id": user_id,
        "full_name": full_name,
        "email": email.lower(),
        "password_hash": hash_password(password),
        "organization": organization,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    db.users.insert_one(user_doc)
    
    return {"success": True, "message": "Account created successfully", "user_id": user_id}


def authenticate_user(email: str, password: str) -> dict:
    """
    Authenticate user with email and password
    Returns: {"success": bool, "message": str, "user": dict or None}
    """
    db = get_auth_db()
    
    user = db.users.find_one({"email": email.lower()})
    
    if not user:
        return {"success": False, "message": "No account found with this email", "user": None}
    
    if user["password_hash"] != hash_password(password):
        return {"success": False, "message": "Incorrect password", "user": None}
    
    # Return user data without password hash
    user_data = {
        "user_id": user["user_id"],
        "full_name": user["full_name"],
        "email": user["email"],
        "organization": user["organization"],
        "created_at": user["created_at"]
    }
    
    return {"success": True, "message": "Login successful", "user": user_data}


def get_user_by_id(user_id: str) -> dict:
    """Get user by user_id"""
    db = get_auth_db()
    user = db.users.find_one({"user_id": user_id})
    
    if user:
        return {
            "user_id": user["user_id"],
            "full_name": user["full_name"],
            "email": user["email"],
            "organization": user["organization"],
            "created_at": user["created_at"]
        }
    return None
