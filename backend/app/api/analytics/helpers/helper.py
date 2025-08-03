import re

def _norm_prompt(p: str) -> str:
    """Fallback key for rows without typeform_ref"""
    p = (p or "").strip().lower()
    p = re.sub(r"\s+", " ", p)
    return f"prompt::{p}"
