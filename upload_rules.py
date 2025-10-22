import requests

API = "http://127.0.0.1:5001/api/mcp/save_rule"

rules = [
    {
        "city": "Mumbai",
        "authority": "MCGM",
        "clause_no": "DCPR 2034-12.3",
        "page": 12,
        "rule_type": "Height",
        "conditions": "Residential zone",
        "entitlements": "Max 7 floors",
        "notes": "Sample Mumbai rule"
    },
    {
        "city": "Ahmedabad",
        "authority": "AUDA",
        "clause_no": "DCR 2021-5.2",
        "page": 5,
        "rule_type": "FSI",
        "conditions": "Commercial zone",
        "entitlements": "FSI 2.5",
        "notes": "Sample Ahmedabad rule"
    }
]

for rule in rules:
    r = requests.post(API, json=rule)
    print(r.json())
