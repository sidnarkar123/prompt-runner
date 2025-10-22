from agent_clients import send_feedback

def rl_agent(case_id, user_feedback):
    """
    Save user feedback to MCP and get reward return.

    user_feedback is "up" or "down".
    """
    result = send_feedback(case_id, user_feedback)
    if result and result.get("success"):
        print(f"[RL Agent] Feedback saved, reward: {result.get('reward')}")
        return result.get('reward')
    else:
        print("[RL Agent] Failed to save feedback")
        return None
