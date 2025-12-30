#!/usr/bin/env python3
"""Debug logging helper for batch files."""
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Find repo root (jptools/debug_log.py -> jptools -> repo root)
SCRIPT_DIR = Path(__file__).parent.resolve()
REPO_ROOT = SCRIPT_DIR.parent
LOG_PATH = REPO_ROOT / ".cursor" / "debug.log"

def log(session_id, run_id, hypothesis_id, location, message, data=None):
    """Write a debug log entry."""
    entry = {
        "id": f"log_{int(datetime.now().timestamp() * 1000)}_{hash(message) % 10000}",
        "timestamp": int(datetime.now().timestamp() * 1000),
        "sessionId": session_id,
        "runId": run_id,
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data or {}
    }
    try:
        # Ensure .cursor directory exists
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        # Write to stderr for debugging if file write fails
        print(f"DEBUG_LOG_ERROR: {e}", file=sys.stderr)
        pass  # Silently fail if logging fails

if __name__ == "__main__":
    if len(sys.argv) < 6:
        sys.exit(1)
    session_id = sys.argv[1]
    run_id = sys.argv[2]
    hypothesis_id = sys.argv[3]
    location = sys.argv[4]
    message = sys.argv[5]
    data_str = sys.argv[6] if len(sys.argv) > 6 else "{}"
    try:
        data = json.loads(data_str) if data_str else {}
    except Exception:
        data = {"raw": data_str}
    log(session_id, run_id, hypothesis_id, location, message, data)
