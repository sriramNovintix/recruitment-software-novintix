import hashlib
from datetime import datetime
from pymongo.errors import DuplicateKeyError
from core.db import init_db

# -------------------------------------------------
# DB + Collection (AUTO-CREATED)
# -------------------------------------------------
db = init_db()
fingerprints_col = db["file_fingerprints"]

# -------------------------------------------------
# AUTO-ENSURE UNIQUE INDEX (SAFE ON EVERY START)
# -------------------------------------------------
fingerprints_col.create_index(
    [
        ("file_hash", 1),
        ("file_type", 1),
        ("jd_id", 1),
    ],
    unique=True,
    name="uniq_file_hash_type_jd"
)

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def _compute_file_hash(file):
    file.seek(0)
    content = file.read()
    file.seek(0)
    return hashlib.md5(content).hexdigest()

# -------------------------------------------------
# PUBLIC API
# -------------------------------------------------
def register_file_or_skip(file, file_type: str, jd_id: str | None = None):
    """
    Atomic duplicate guard.

    Returns:
        (True, None)  -> New file, safe to process
        (False, name) -> Duplicate file, skipped
    """
    file_hash = _compute_file_hash(file)

    try:
        fingerprints_col.insert_one({
            "file_hash": file_hash,
            "file_type": file_type,  # "jd" | "resume"
            "jd_id": jd_id,          # scoped for resumes
            "file_name": file.name,
            "created_at": datetime.utcnow()
        })
        return True, None

    except DuplicateKeyError:
        return False, file.name