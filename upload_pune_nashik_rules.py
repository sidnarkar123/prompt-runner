"""
Upload Pune and Nashik Rules to MCP Database
---------------------------------------------
This script uploads the Pune and Nashik development control rules
from mcp_data/rules.json to the MongoDB MCP database.

Usage:
    python upload_pune_nashik_rules.py
"""

import os
import json
import requests
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MCP API endpoint
MCP_API_BASE = "http://127.0.0.1:5001/api/mcp"
SAVE_RULE_ENDPOINT = f"{MCP_API_BASE}/save_rule"

# Path to rules file
RULES_FILE = Path("mcp_data/rules.json")


def load_rules():
    """Load rules from JSON file."""
    if not RULES_FILE.exists():
        logger.error(f"Rules file not found: {RULES_FILE}")
        return {}
    
    with open(RULES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def upload_city_rules(city: str, rules: list):
    """Upload all rules for a specific city to MCP."""
    logger.info(f"Uploading {len(rules)} rules for {city}...")
    
    uploaded = 0
    failed = 0
    
    for rule_data in rules:
        try:
            # Prepare payload
            rule_obj = rule_data.get("rule", {})
            payload = {
                "city": city,
                "authority": rule_obj.get("authority"),
                "clause_no": rule_obj.get("clause_no"),
                "page": rule_obj.get("page"),
                "rule_type": rule_obj.get("rule_type"),
                "conditions": rule_obj.get("conditions"),
                "entitlements": rule_obj.get("entitlements"),
                "notes": rule_obj.get("notes"),
                "parsed_fields": rule_obj.get("parsed_fields", {})
            }
            
            # Send to MCP
            response = requests.post(SAVE_RULE_ENDPOINT, json=payload, timeout=10)
            
            if response.status_code in (200, 201):
                result = response.json()
                if result.get("success"):
                    uploaded += 1
                    logger.info(f"  ✅ Uploaded: {rule_obj.get('clause_no')}")
                else:
                    failed += 1
                    logger.error(f"  ❌ Failed: {rule_obj.get('clause_no')} - {result}")
            else:
                failed += 1
                logger.error(f"  ❌ HTTP {response.status_code}: {rule_obj.get('clause_no')}")
        
        except Exception as e:
            failed += 1
            logger.error(f"  ❌ Error uploading rule: {e}")
    
    logger.info(f"  {city}: {uploaded} uploaded, {failed} failed")
    return uploaded, failed


def main():
    """Main upload function."""
    logger.info("=" * 60)
    logger.info("Uploading Pune and Nashik Rules to MCP Database")
    logger.info("=" * 60)
    
    # Load all rules
    all_rules = load_rules()
    
    if not all_rules:
        logger.error("No rules loaded. Exiting.")
        return
    
    logger.info(f"Loaded rules for cities: {', '.join(all_rules.keys())}")
    
    # Track totals
    total_uploaded = 0
    total_failed = 0
    
    # Upload Pune rules
    if "Pune" in all_rules:
        logger.info("\n📍 Processing Pune...")
        uploaded, failed = upload_city_rules("Pune", all_rules["Pune"])
        total_uploaded += uploaded
        total_failed += failed
    else:
        logger.warning("⚠️  No Pune rules found in rules.json")
    
    # Upload Nashik rules
    if "Nashik" in all_rules:
        logger.info("\n📍 Processing Nashik...")
        uploaded, failed = upload_city_rules("Nashik", all_rules["Nashik"])
        total_uploaded += uploaded
        total_failed += failed
    else:
        logger.warning("⚠️  No Nashik rules found in rules.json")
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("UPLOAD SUMMARY")
    logger.info("=" * 60)
    logger.info(f"✅ Total Uploaded: {total_uploaded}")
    logger.info(f"❌ Total Failed: {total_failed}")
    logger.info("=" * 60)
    
    if total_failed == 0:
        logger.info("🎉 All rules uploaded successfully!")
    else:
        logger.warning(f"⚠️  {total_failed} rules failed to upload. Check logs above.")


def verify_upload():
    """Verify the upload by listing rules from MCP."""
    logger.info("\n" + "=" * 60)
    logger.info("VERIFICATION: Listing rules from MCP")
    logger.info("=" * 60)
    
    try:
        response = requests.get(f"{MCP_API_BASE}/list_rules?limit=50", timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                rules = result.get("rules", [])
                
                # Count by city
                city_counts = {}
                for rule in rules:
                    city = rule.get("city", "Unknown")
                    city_counts[city] = city_counts.get(city, 0) + 1
                
                logger.info(f"Total rules in database: {result.get('count')}")
                for city, count in sorted(city_counts.items()):
                    logger.info(f"  {city}: {count} rules")
            else:
                logger.error("Failed to fetch rules from MCP")
        else:
            logger.error(f"HTTP {response.status_code} when fetching rules")
    except Exception as e:
        logger.error(f"Error verifying upload: {e}")


if __name__ == "__main__":
    # Check if MCP server is running
    try:
        response = requests.get(MCP_API_BASE.replace("/api/mcp", "/"), timeout=5)
        if response.status_code != 200:
            logger.error("❌ MCP server not responding. Please start it first:")
            logger.error("   python mcp_server.py")
            exit(1)
    except requests.exceptions.ConnectionError:
        logger.error("❌ Cannot connect to MCP server at http://127.0.0.1:5001")
        logger.error("   Please start the MCP server first:")
        logger.error("   python mcp_server.py")
        exit(1)
    
    # Run upload
    main()
    
    # Verify
    verify_upload()

