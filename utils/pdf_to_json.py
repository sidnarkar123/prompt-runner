import os
import json
import datetime
from utils import mcp_store

# --- Folders ---
DOWNLOADS_DIR = r"C:\Users\sid\Desktop\prompt runner\streamlit-prompt-runner\downloads"
JSON_OUTPUT_DIR = os.path.join(DOWNLOADS_DIR, "json_rules")
os.makedirs(JSON_OUTPUT_DIR, exist_ok=True)

# --- Fake PDF paths ---
PDF_PATHS = {
    "Mumbai": r"C:\Users\sid\Documents\Mumbai_DCPR_Fake.pdf",
    "Ahmedabad": r"C:\Users\sid\Documents\Ahmedabad_DCR_Fake.pdf",
    "Pune": r"C:\Users\sid\Documents\Pune_DCR_Fake.pdf",
    "Nashik": r"C:\Users\sid\Documents\Nashik_DCR_Fake.pdf"
}

# --- Function to parse PDF (simulate) ---
def parse_pdf_to_json(city, pdf_path):
    # Simulate extracting rules
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    rule_json = {
        "city": city,
        "pdf_source": pdf_path,
        "rules": [
            {"clause_no": "12.1", "conditions": "Condition A", "entitlements": "Entitlement 1"},
            {"clause_no": "12.2", "conditions": "Condition B", "entitlements": "Entitlement 2"}
        ],
        "timestamp": timestamp
    }

    # Save JSON locally
    json_filename = f"rule_{city}_{timestamp}.json"
    json_path = os.path.join(JSON_OUTPUT_DIR, json_filename)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rule_json, f, indent=2)

    # Push to MCP
    meta = {"source_pdf": pdf_path, "timestamp": timestamp}
    for r in rule_json["rules"]:
        mcp_store.save_rule(city=city, rule=r, meta=meta)

    print(f"[{city}] Parsed PDF → JSON saved at {json_path} and pushed to MCP.")
    return json_path

# --- Main loop ---
if __name__ == "__main__":
    for city, pdf_path in PDF_PATHS.items():
        if os.path.exists(pdf_path):
            parse_pdf_to_json(city, pdf_path)
        else:
            print(f"[{city}] PDF not found at {pdf_path}, skipping.")
