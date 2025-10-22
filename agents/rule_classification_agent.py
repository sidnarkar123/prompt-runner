import requests

API = "http://127.0.0.1:5001/api/mcp/rules"
rules = requests.get(API).json()

for rule in rules:
    print(f"Rule {rule['id']} ({rule['city']}): {rule['rule_type']}")
    # Add classification logic here
