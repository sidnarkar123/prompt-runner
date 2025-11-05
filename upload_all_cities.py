#!/usr/bin/env python3
"""
Upload all city rules (Mumbai, Ahmedabad, Pune, Nashik) to MCP MongoDB
"""
import json
import requests
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MCP_API_URL = "http://127.0.0.1:5001/api/mcp/save_rule"
RULES_FILE = Path("mcp_data/rules.json")


def upload_rules():
    """Upload all rules from rules.json to MCP database"""
    
    if not RULES_FILE.exists():
        logger.error(f"Rules file not found: {RULES_FILE}")
        return
    
    with open(RULES_FILE, 'r', encoding='utf-8') as f:
        all_rules = json.load(f)
    
    total_uploaded = 0
    total_failed = 0
    
    for city, rules in all_rules.items():
        logger.info(f"\n📍 Uploading rules for {city}...")
        
        for rule_entry in rules:
            rule_data = rule_entry.get("rule", {})
            meta = rule_entry.get("meta", {})
            
            # Prepare payload for MCP API
            payload = {
                "city": city,
                "authority": rule_data.get("authority", meta.get("authority")),
                "clause_no": rule_data.get("clause_no"),
                "page": rule_data.get("page"),
                "rule_type": rule_data.get("rule_type"),
                "conditions": rule_data.get("conditions"),
                "entitlements": rule_data.get("entitlements"),
                "notes": rule_data.get("notes", ""),
                "parsed_fields": rule_data.get("parsed_fields", {})
            }
            
            try:
                response = requests.post(MCP_API_URL, json=payload, timeout=10)
                
                if response.status_code in (200, 201):
                    result = response.json()
                    if result.get("success"):
                        logger.info(f"  ✅ Uploaded: {rule_data.get('clause_no')}")
                        total_uploaded += 1
                    else:
                        logger.error(f"  ❌ Failed: {rule_data.get('clause_no')} - {result.get('error')}")
                        total_failed += 1
                else:
                    logger.error(f"  ❌ HTTP {response.status_code}: {rule_data.get('clause_no')}")
                    total_failed += 1
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"  ❌ Network error for {rule_data.get('clause_no')}: {e}")
                total_failed += 1
            except Exception as e:
                logger.error(f"  ❌ Error uploading {rule_data.get('clause_no')}: {e}")
                total_failed += 1
    
    logger.info(f"\n{'='*60}")
    logger.info(f"📊 Upload Summary:")
    logger.info(f"  ✅ Successfully uploaded: {total_uploaded}")
    logger.info(f"  ❌ Failed: {total_failed}")
    logger.info(f"  📦 Total: {total_uploaded + total_failed}")
    logger.info(f"{'='*60}\n")
    
    return total_uploaded, total_failed


def verify_upload():
    """Verify rules were uploaded by fetching them from MCP"""
    list_url = "http://127.0.0.1:5001/api/mcp/list_rules"
    
    try:
        response = requests.get(list_url, params={"limit": 1000}, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                count = result.get("count", 0)
                logger.info(f"✅ Verification: Found {count} rules in MCP database")
                
                # Count by city
                rules = result.get("rules", [])
                city_counts = {}
                for rule in rules:
                    city = rule.get("city", "Unknown")
                    city_counts[city] = city_counts.get(city, 0) + 1
                
                logger.info(f"\n📊 Rules by City:")
                for city, count in sorted(city_counts.items()):
                    logger.info(f"  {city}: {count} rules")
            else:
                logger.error("Failed to verify upload")
        else:
            logger.error(f"HTTP {response.status_code} when verifying")
    except Exception as e:
        logger.error(f"Error verifying upload: {e}")


if __name__ == "__main__":
    logger.info("🚀 Starting MCP Rules Upload")
    logger.info(f"📁 Reading from: {RULES_FILE.absolute()}")
    logger.info(f"🔗 Uploading to: {MCP_API_URL}\n")
    
    # Check if MCP server is running
    try:
        health_check = requests.get("http://127.0.0.1:5001/", timeout=5)
        if health_check.status_code == 200:
            logger.info("✅ MCP Server is running\n")
        else:
            logger.warning("⚠️ MCP Server might not be running properly\n")
    except requests.exceptions.RequestException:
        logger.error("❌ MCP Server is not running!")
        logger.error("   Please start it with: python mcp_server.py")
        exit(1)
    
    # Upload rules
    uploaded, failed = upload_rules()
    
    # Verify
    if uploaded > 0:
        logger.info("\n🔍 Verifying upload...")
        verify_upload()
    
    logger.info("\n✨ Done!")
