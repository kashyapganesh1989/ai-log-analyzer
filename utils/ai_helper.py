"""
ai_helper.py
-------------
Utility module to analyze logs using OpenAI GPT.
"""
import os
import re
from openai import OpenAI
from dotenv import load_dotenv

# Load OpenAI API key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def sanitize_log_text(log_text):
    """
    Redact sensitive info before sending to OpenAI:
    - File paths
    - IP addresses
    - Usernames
    """
    # Replace absolute paths
    log_text = re.sub(r"/[A-Za-z0-9_\-\/\.]+", "[PATH_REDACTED]", log_text)
    
    # Replace IP addresses
    log_text = re.sub(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", "[IP_REDACTED]", log_text)
    
    # Replace usernames
    log_text = re.sub(r"user\s+\w+", "user [REDACTED]", log_text, flags=re.IGNORECASE)
    
    return log_text


def analyze_with_ai(log_text):
    """
    Send logs to OpenAI GPT for analysis.
    Returns a structured, human-readable report with:
    - Log snippet
    - Probable Root Cause
    - Suggested Resolution
    """
    sanitized_logs = sanitize_log_text(log_text)

    prompt = f"""
You are an expert IT operations assistant. Analyze the following application logs and identify each distinct issue.

For each issue, provide:
1. Log snippet (a short 1-line excerpt from the log)
2. Probable Root Cause (explain briefly)
3. Suggested Resolution (practical fix or next step)
4. Severity (one of: Info, Warning, Error, Critical)

Format your answer EXACTLY as below:

Log snippet: <excerpt>
Probable Root Cause: <cause>
Suggested Resolution: <resolution>
Severity: <level>

Separate multiple issues with one blank line.

Logs:
{sanitized_logs}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        ai_output = response.choices[0].message.content.strip()
        return ai_output

    except Exception as e:
        return f"⚠️ Error analyzing logs with OpenAI: {e}"

def parse_ai_report(ai_report):
    """
    Parses AI response into structured issues.
    Looks for keywords instead of relying on emojis.
    """
    issues = []
    blocks = re.split(r"\n\s*\n", ai_report)
    
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        
        issue_match = re.search(r"(?:Log snippet|Issue|Error|Warning)[:\-]\s*(.+)", block, re.IGNORECASE)
        cause_match = re.search(r"(?:Probable Root Cause|Cause)[:\-]\s*(.+)", block, re.IGNORECASE)
        resolution_match = re.search(r"(?:Suggested Resolution|Resolution)[:\-]\s*(.+)", block, re.IGNORECASE)
        severity_match = re.search(r"(?:Severity)[:\-]\s*(.+)", block, re.IGNORECASE)

        if issue_match:
            issues.append({
                "Issue": issue_match.group(1).strip(),
                "Cause": cause_match.group(1).strip() if cause_match else "",
                "Resolution": resolution_match.group(1).strip() if resolution_match else "",
                "Severity": severity_match.group(1).strip() if severity_match else "Info"
            })
    return issues

