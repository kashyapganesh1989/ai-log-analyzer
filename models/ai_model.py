import re
from transformers import pipeline

def analyze_log_ai(log_lines):
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    issues = []
    for line in log_lines:
        if "error" in line.lower() or "exception" in line.lower():
            labels = ["syntax error", "file not found", "connection issue", "permission denied", "memory leak"]
            result = classifier(line, labels)
            issues.append({
                "log_line": line,
                "error": result['labels'][0],
                "cause": "Auto-identified by AI model"
            })
    return issues
