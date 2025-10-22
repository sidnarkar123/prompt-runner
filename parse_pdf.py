import sys
import json
from PyPDF2 import PdfReader

def parse_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    # Simple text extraction for demo
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    # Here you'd add programming logic to convert text to JSON rules
    rules = [{
        "city": "Mumbai",
        "clause_no": "DCPR 2034-12.3",
        "rule": "Height <= 24m",
        "authority": "MCGM",
        "conditions": "Residential zone",
        "entitlements": "Max 7 floors",
        "notes": "",
        "extracted_text": text[:100]  # sample excerpt
    }]
    print(json.dumps(rules))  # output JSON

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: parse_pdf.py <pdf_path>")
        sys.exit(1)
    parse_pdf(sys.argv[1])
