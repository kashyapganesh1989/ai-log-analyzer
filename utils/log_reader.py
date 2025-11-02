"""
log_reader.py
--------------
Utility module to read logs from a single file or a directory.

Supported:
- UNIX logs
- Java logs
- Python logs
- Ab Initio logs (.log, .txt)
"""

import os


def read_logs(path):
    """
    Reads all log files from the given path.
    If the path is a file, reads that file only.
    If it's a directory, recursively reads all .log and .txt files.
    Returns the combined log content as a string.
    """

    logs = []
    path = os.path.abspath(path)

    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                logs.append(f.read())
        except Exception as e:
            print(f"⚠️ Error reading file {path}: {e}")

    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for f in files:
                if f.lower().endswith((".log", ".txt")):
                    file_path = os.path.join(root, f)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            logs.append(content)
                    except Exception as e:
                        print(f"⚠️ Skipping {file_path}: {e}")
    else:
        raise FileNotFoundError(f"❌ Path not found: {path}")

    combined_logs = "\n".join(logs).strip()
    if not combined_logs:
        combined_logs = "No readable log content found."

    return combined_logs


def summarize_log_size(path):
    """
    Provides a simple summary (number of files, total size in KB)
    to display in the UI before AI analysis.
    """
    total_files = 0
    total_size = 0

    if os.path.isfile(path):
        return {"files": 1, "size_kb": round(os.path.getsize(path) / 1024, 2)}

    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for f in files:
                if f.lower().endswith((".log", ".txt")):
                    total_files += 1
                    try:
                        total_size += os.path.getsize(os.path.join(root, f))
                    except Exception:
                        pass

    return {"files": total_files, "size_kb": round(total_size / 1024, 2)}
