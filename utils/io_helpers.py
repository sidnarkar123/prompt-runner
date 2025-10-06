# ...existing code...
import os
import json
from datetime import datetime
from uuid import uuid4

# === Directory Setup ===
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))  # points to project root: streamlit-prompt-runner
PROMPTS_DIR = os.path.join(ROOT_DIR, "prompts")
SPECS_DIR = os.path.join(ROOT_DIR, "specs")
LOGS_DIR = os.path.join(ROOT_DIR, "logs")
SEND_EVAL_DIR = os.path.join(ROOT_DIR, "send_to_evaluator")
SEND_UNREAL_DIR = os.path.join(ROOT_DIR, "send_to_unreal")

PROMPT_LOG = os.path.join(LOGS_DIR, "prompt_logs.json")
ACTION_LOG = os.path.join(LOGS_DIR, "action_logs.json")


# === Ensure directories and log files ===
def _ensure_dirs():
    """
    Ensure required directories exist. 
    If a required path exists but is a file, rename it safely and recreate the folder.
    """
    for d in (PROMPTS_DIR, SPECS_DIR, LOGS_DIR, SEND_EVAL_DIR, SEND_UNREAL_DIR):
        if os.path.exists(d) and not os.path.isdir(d):
            bak = d + ".bak"
            i = 1
            while os.path.exists(bak):
                bak = f"{d}.bak{i}"
                i += 1
            os.rename(d, bak)
        os.makedirs(d, exist_ok=True)

    # Ensure log files exist
    for log_path in (PROMPT_LOG, ACTION_LOG):
        if os.path.isdir(log_path):
            bak = log_path + ".bak"
            i = 1
            while os.path.exists(bak):
                bak = f"{log_path}.bak{i}"
                i += 1
            os.rename(log_path, bak)
        if not os.path.exists(log_path):
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump([], f)


# === Utility JSON functions ===
def _read_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _normalize_logs_list(raw):
    """
    Normalize various log structures into a clean list of entries.
    Handles legacy formats like dict wrappers and id->entry mappings.
    """
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        if isinstance(raw.get("prompt_logs"), list):
            return raw["prompt_logs"]
        if isinstance(raw.get("prompts"), list):
            return raw["prompts"]
        vals = [v for v in raw.values() if isinstance(v, dict)]
        if vals:
            return vals
    return []


# === Save Prompt ===
def save_prompt(prompt_text: str) -> str:
    """
    Save a raw prompt to /prompts and append a record in /logs/prompt_logs.json.
    Returns the prompt ID.
    """
    _ensure_dirs()
    if not prompt_text:
        raise ValueError("Prompt must be non-empty")

    pid = uuid4().hex[:8]
    timestamp = datetime.utcnow().isoformat() + "Z"
    prompt_filename = f"{pid}.txt"
    with open(os.path.join(PROMPTS_DIR, prompt_filename), "w", encoding="utf-8") as f:
        f.write(prompt_text)

    logs_raw = _read_json(PROMPT_LOG, [])
    logs = _normalize_logs_list(logs_raw)

    entry = {
        "id": pid,
        "timestamp": timestamp,
        "prompt": prompt_text,
        "spec_filename": None
    }
    logs.append(entry)
    _write_json(PROMPT_LOG, logs)
    return pid


# === Save Spec ===
def save_spec(spec: dict) -> str:
    """
    Save a spec dict to /specs/<id>.json.
    Attach it to the most recent prompt without a spec.
    Returns the spec filename.
    """
    _ensure_dirs()
    if not isinstance(spec, dict):
        raise ValueError("spec must be a dict")

    logs_raw = _read_json(PROMPT_LOG, [])
    logs = _normalize_logs_list(logs_raw)

    target = None
    for entry in reversed(logs):
        if not entry.get("spec_filename"):
            target = entry
            break

    if target is None:
        pid = uuid4().hex[:8]
        timestamp = datetime.utcnow().isoformat() + "Z"
        target = {"id": pid, "timestamp": timestamp, "prompt": "", "spec_filename": None}
        logs.append(target)

    spec_filename = f"{target['id']}.json"
    _write_json(os.path.join(SPECS_DIR, spec_filename), spec)

    target["spec_filename"] = spec_filename
    _write_json(PROMPT_LOG, logs)
    return spec_filename


# === Load Prompts ===
def load_prompts() -> list:
    """
    Return a list of available prompt IDs in chronological order.
    Handles mixed or legacy JSON shapes gracefully.
    """
    _ensure_dirs()
    logs_raw = _read_json(PROMPT_LOG, [])
    logs = _normalize_logs_list(logs_raw)

    ids = []
    for entry in logs:
        if isinstance(entry, dict):
            eid = entry.get("id") or entry.get("prompt_id") or entry.get("spec_filename") or entry.get("filename")
            if isinstance(eid, str) and eid:
                eid = os.path.splitext(os.path.basename(eid))[0]
                ids.append(eid)
        elif isinstance(entry, str):
            ids.append(os.path.splitext(os.path.basename(entry))[0])

    seen = set()
    uniq_ids = []
    for i in ids:
        if i not in seen:
            seen.add(i)
            uniq_ids.append(i)

    return uniq_ids


# === Load All Logs ===
def load_logs() -> dict:
    """
    Return both prompt and action logs.
    """
    _ensure_dirs()
    return {
        "prompt_logs": _read_json(PROMPT_LOG, []),
        "action_logs": _read_json(ACTION_LOG, [])
    }


# === Log Action ===
def log_action(action_type: str, spec_id: str, details: dict = None):
    """
    Append a routing/action event to /logs/action_logs.json.
    """
    _ensure_dirs()
    actions = _read_json(ACTION_LOG, [])
    actions.append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action_type,
        "spec_id": spec_id,
        "details": details or {}
    })
    _write_json(ACTION_LOG, actions)
