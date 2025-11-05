# agents/rl_agent.py
import logging
from datetime import datetime
import json
import os
from agents.agent_clients import send_feedback

logging.basicConfig(level=logging.INFO)
TRAIN_LOG = "rl_training_logs.json"
os.makedirs(os.path.dirname(TRAIN_LOG) or ".", exist_ok=True)

def rl_agent_submit_feedback(case_id: str, user_feedback: str, metadata: dict = None) -> int:
    """
    user_feedback: "up" or "down"
    returns reward (int) or None on failure
    """
    metadata = metadata or {}
    resp = send_feedback(case_id, user_feedback)
    reward = None
    if resp and isinstance(resp, dict) and resp.get("success"):
        reward = resp.get("reward")
    else:
        logging.error("Failed to send feedback to MCP for %s", case_id)
        return None

    # Persist local training record for later offline RL training
    record = {
        "case_id": case_id,
        "feedback": user_feedback,
        "reward": reward,
        "meta": metadata,
        "timestamp": datetime.utcnow().isoformat()+"Z"
    }

    # append to local training log
    logs = []
    if os.path.exists(TRAIN_LOG):
        try:
            with open(TRAIN_LOG, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except Exception:
            logs = []
    logs.append(record)
    with open(TRAIN_LOG, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)

    logging.info("RL feedback recorded: %s -> %s (reward=%s)", case_id, user_feedback, reward)
    return reward
