import requests

MCP_BASE_URL = "http://localhost:5001/api/mcp"

def save_rule(rule_json):
    try:
        response = requests.post(f"{MCP_BASE_URL}/save_rule", json=rule_json)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error saving rule: {e}")
        return None

def get_rules(city):
    try:
        response = requests.get(f"{MCP_BASE_URL}/list_rules")
        response.raise_for_status()
        all_rules = response.json().get("rules", [])
        return [r for r in all_rules if r.get("city", "").lower() == city.lower()]
    except requests.RequestException as e:
        print(f"Error retrieving rules: {e}")
        return []

def send_feedback(case_id, feedback):
    data = {"case_id": case_id, "feedback": feedback}
    try:
        response = requests.post(f"{MCP_BASE_URL}/feedback", json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error sending feedback: {e}")
        return None

def log_geometry(case_id, file_path):
    data = {"case_id": case_id, "file": file_path}
    try:
        response = requests.post(f"{MCP_BASE_URL}/geometry", json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error logging geometry: {e}")
        return None
