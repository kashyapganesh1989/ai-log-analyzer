import json
import os

def suggest_resolution(error):
    kb_path = os.path.join("data", "knowledge_base.json")
    with open(kb_path, "r") as f:
        kb = json.load(f)
    return kb.get(error.lower(), "No direct resolution found. Please review manually.")
