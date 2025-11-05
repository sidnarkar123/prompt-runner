#io_helpers.py
import os
import json
from datetime import datetime

SPEC_DIR = "specs"
SEND_EVAL_DIR = "SEND_EVAL"
SEND_UNREAL_DIR = "SEND_UNREAL"
PROMPT_LOG = "prompt_logs.json"
ACTION_LOG = "action_logs.json"

os.makedirs(SPEC_DIR, exist_ok=True)
os.makedirs(SEND_EVAL_DIR, exist_ok=True)
os.makedirs(SEND_UNREAL_DIR, exist_ok=True)

def save_spec(spec):
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"{ts}.json"
    path = os.path.join(SPEC_DIR, filename)
    with open(path, "w") as f:
        json.dump(spec, f, indent=2)
    return filename

def save_prompt(prompt, spec_filename):
    logs = load_prompts()
    entry = {
        "id": spec_filename.replace(".json",""),
        "prompt": prompt,
        "spec_filename": spec_filename,
        "timestamp": datetime.utcnow().isoformat()+"Z"
    }
    logs.append(entry)
    with open(PROMPT_LOG, "w") as f:
        json.dump(logs, f, indent=2)

def load_prompts():
    if not os.path.exists(PROMPT_LOG):
        return []
    with open(PROMPT_LOG) as f:
        return json.load(f)

def log_action(action, spec_id, details=None):
    logs = load_logs().get("action_logs", [])
    entry = {
        "timestamp": datetime.utcnow().isoformat()+"Z",
        "action": action,
        "spec_id": spec_id,
        "details": details or {}
    }
    logs.append(entry)
    with open(ACTION_LOG, "w") as f:
        json.dump(logs, f, indent=2)

def load_logs():
    logs = {}
    if os.path.exists(PROMPT_LOG):
        with open(PROMPT_LOG) as f:
            logs["prompt_logs"] = json.load(f)
    else:
        logs["prompt_logs"] = []

    if os.path.exists(ACTION_LOG):
        with open(ACTION_LOG) as f:
            logs["action_logs"] = json.load(f)
    else:
        logs["action_logs"] = []

    return logs
