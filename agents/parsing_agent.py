import requests
import json

def parse_pdf_to_json(pdf_path):
    # Dummy function, replace with real parsing logic
    return {
        "city": "Mumbai",
        "authority": "MCGM",
        "clause_no": "DCPR 2034-12.3",
        "page": 12,
        "rule_type": "Height",
        "conditions": "Residential zone",
        "entitlements": "Max 7 floors",
        "notes": "Parsed from PDF"
    }

API = "http://127.0.0.1:5001/api/mcp/save_rule"
parsed_rule = parse_pdf_to_json("sample.pdf")
r = requests.post(API, json=parsed_rule)
print(r.json())
