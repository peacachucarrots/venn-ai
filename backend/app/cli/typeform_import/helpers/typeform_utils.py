import re, hashlib, json, os, requests

number_re = re.compile(r"^\s*(\d+(?:\.\d+)?)")
def _num_val(label: str) -> float | None:
    """Pull leading 1, 1.5, 2 … number from a choice label, else None."""
    m = number_re.match(label)
    return float(m.group(1)) if m else None

def _hash_schema(form_json: dict) -> str:
    """Stable hash of Typeform field structure so we can detect no-ops"""
    sig = [(f["ref"], f["type"],
            [c["ref"] for c in f.get("properties", {}).get("choices", [])])
           for f in form_json["fields"]]
    return hashlib.sha1(json.dumps(sig, sort_keys=True).encode()).hexdigest()

def fetch_json(form_id: str) -> dict:
    """Returns typeform survey in json format"""
    res = requests.get(
        f"https://api.typeform.com/forms/{form_id}",
        headers={"Authorization": f"Bearer {os.environ['TYPEFORM_TOKEN']}"},
        timeout=20,
    )
    res.raise_for_status()
    form = res.json()

    return form
