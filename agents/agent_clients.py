# agents/agent_clients.py
import requests
from typing import List, Dict, Optional
import logging
import os

logging.basicConfig(level=logging.INFO)
MCP_BASE = os.environ.get("MCP_BASE_URL", "http://127.0.0.1:5001/api/mcp")

def _post(path: str, payload: dict) -> Optional[dict]:
    url = f"{MCP_BASE}{path}"
    try:
        r = requests.post(url, json=payload, timeout=8)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logging.error("POST %s failed: %s", url, e)
        return None

def _get(path: str) -> Optional[dict]:
    url = f"{MCP_BASE}{path}"
    try:
        r = requests.get(url, timeout=8)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logging.error("GET %s failed: %s", url, e)
        return None

# ---- Public APIs ----

def save_rule(rule_json: dict) -> Optional[dict]:
    return _post("/save_rule", rule_json)

def list_rules() -> List[dict]:
    res = _get("/list_rules")
    return res.get("rules", []) if res else []

def get_rules_for_city(city: str) -> List[dict]:
    all_rules = list_rules()
    return [r for r in all_rules if r.get("city", "").lower() == city.lower()]

def send_feedback(case_id: str, feedback: str) -> Optional[dict]:
    return _post("/feedback", {"case_id": case_id, "feedback": feedback})

def log_geometry(case_id: str, file_path: str) -> Optional[dict]:
    return _post("/geometry", {"case_id": case_id, "file": file_path})

def upload_parsed_pdf(case_id: str, parsed_data: dict) -> Optional[dict]:
    """
    Push parsed PDF (JSON format) into MCP backend for storage.
    """
    payload = {
        "case_id": case_id,
        "parsed_data": parsed_data
    }
    return _post("/upload_parsed_pdf", payload)
