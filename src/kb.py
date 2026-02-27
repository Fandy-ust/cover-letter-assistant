import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# Directory definitions
RAW_MATERIALS_DIR = BASE_DIR / "raw_materials"
REFERENCE_DRAFTS_DIR = RAW_MATERIALS_DIR / "reference_drafts"
MY_INFO_DIR = BASE_DIR / "my_info"
KNOWLEDGE_DIR = BASE_DIR / "knowledge"
WORKSPACE_DIR = BASE_DIR / "workspace"

# Ensure directories exist
for d in [RAW_MATERIALS_DIR, REFERENCE_DRAFTS_DIR, MY_INFO_DIR, KNOWLEDGE_DIR, WORKSPACE_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# File path definitions
PERSONAL_PROFILE_PATH = MY_INFO_DIR / "personal_profile.md"
STYLE_GUIDELINES_PATH = KNOWLEDGE_DIR / "style_guidelines.md"
APPLICATION_BRIEF_PATH = WORKSPACE_DIR / "application_brief.md"
FINAL_DRAFT_PATH = WORKSPACE_DIR / "final_draft.md"
ADVISOR_CHAT_LOG_PATH = WORKSPACE_DIR / "advisor_chat_log.md"

def _read_file(path: Path) -> str:
    """Reads a text file gracefully. Returns empty string if not found."""
    if not path.exists():
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return ""

def _write_file(path: Path, content: str):
    """Writes a text file gracefully."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing {path}: {e}")

def _append_file(path: Path, content: str):
    """Appends to a text file gracefully."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"Error appending to {path}: {e}")

# --- Personal Profile ---
def read_personal_profile() -> str:
    return _read_file(PERSONAL_PROFILE_PATH)

def write_personal_profile(content: str):
    _write_file(PERSONAL_PROFILE_PATH, content)

def append_to_personal_profile(content: str):
    """Useful for the Profile Builder to append new experiences."""
    # Add a newline if appending
    _append_file(PERSONAL_PROFILE_PATH, "\n" + content)

# --- Style Guidelines ---
def read_style_guidelines() -> str:
    return _read_file(STYLE_GUIDELINES_PATH)

def write_style_guidelines(content: str):
    _write_file(STYLE_GUIDELINES_PATH, content)

def append_to_style_guidelines(content: str):
    _append_file(STYLE_GUIDELINES_PATH, "\n" + content)

# --- Workspace Files ---
def read_application_brief() -> str:
    return _read_file(APPLICATION_BRIEF_PATH)

def write_application_brief(content: str):
    _write_file(APPLICATION_BRIEF_PATH, content)

def read_final_draft() -> str:
    return _read_file(FINAL_DRAFT_PATH)

def write_final_draft(content: str):
    _write_file(FINAL_DRAFT_PATH, content)

def read_advisor_chat_log() -> str:
    return _read_file(ADVISOR_CHAT_LOG_PATH)

def write_advisor_chat_log(content: str):
    _write_file(ADVISOR_CHAT_LOG_PATH, content)

def get_job_description_image_path() -> Path | None:
    """Returns the path to the job description image if it exists."""
    for ext in ["png", "jpg", "jpeg"]:
        img_path = WORKSPACE_DIR / f"job_description.{ext}"
        if img_path.exists():
            return img_path
    return None

def save_job_description_image(file_bytes: bytes, filename: str) -> Path:
    """Saves an uploaded job description image to the workspace."""
    ext = filename.split(".")[-1].lower()
    if ext not in ["png", "jpg", "jpeg"]:
        ext = "png" # default fallback
    
    save_path = WORKSPACE_DIR / f"job_description.{ext}"
    try:
        with open(save_path, "wb") as f:
            f.write(file_bytes)
        return save_path
    except Exception as e:
        print(f"Error saving job description image: {e}")
        return save_path

# --- Raw Materials & Reference Drafts ---
def get_raw_materials_files() -> list[Path]:
    """Returns a list of files in the raw_materials directory."""
    if not RAW_MATERIALS_DIR.exists():
        return []
    return [p for p in RAW_MATERIALS_DIR.iterdir() if p.is_file() and not p.name.startswith('.')]

def get_reference_drafts_files() -> list[Path]:
    """Returns a list of files in the reference_drafts directory."""
    if not REFERENCE_DRAFTS_DIR.exists():
        return []
    return [p for p in REFERENCE_DRAFTS_DIR.iterdir() if p.is_file() and not p.name.startswith('.')]

def save_raw_material(file_bytes: bytes, filename: str) -> Path:
    save_path = RAW_MATERIALS_DIR / filename
    try:
        with open(save_path, "wb") as f:
            f.write(file_bytes)
        return save_path
    except Exception as e:
        print(f"Error saving raw material: {e}")
        return save_path

def save_reference_draft(file_bytes: bytes, filename: str) -> Path:
    save_path = REFERENCE_DRAFTS_DIR / filename
    try:
        with open(save_path, "wb") as f:
            f.write(file_bytes)
        return save_path
    except Exception as e:
        print(f"Error saving reference draft: {e}")
        return save_path
