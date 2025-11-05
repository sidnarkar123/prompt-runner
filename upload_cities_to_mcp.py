"""
Upload Pune and Nashik city rules to MCP MongoDB database
"""
import requests
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MCP_API_BASE = "http://127.0.0.1:5001/api/mcp"

def upload_city_rules(city_name: str, rules: list):
    """Upload all rules for a specific city to MCP"""
    success_count = 0
    fail_count = 0
    
    logger.info(f"📤 Uploading {len(rules)} rules for {city_name}...")
    
    for rule_data in rules:
        try:
            # Extract rule from nested structure
            rule = rule_data.get("rule", {})
            
            # Prepare payload for MCP
            payload = {
                "city": city_name,
                "authority": rule.get("authority"),
                "clause_no": rule.get("clause_no"),
                "page": rule.get("page"),
                "rule_type": rule.get("rule_type"),
                "conditions": rule.get("conditions"),
                "entitlements": rule.get("entitlements"),
                "notes": rule.get("notes", ""),
                "parsed_fields": rule.get("parsed_fields", {}),
                "created_at": datetime.utcnow().isoformat() + "Z"
            }
            
            # Send to MCP
            response = requests.post(f"{MCP_API_BASE}/save_rule", json=payload)
            
            if response.status_code == 201:
                result = response.json()
                logger.info(f"  ✅ {rule.get('clause_no')} - ID: {result.get('inserted_id', 'N/A')}")
                success_count += 1
            else:
                logger.error(f"  ❌ Failed to upload {rule.get('clause_no')}: {response.text}")
                fail_count += 1
                
        except Exception as e:
            logger.error(f"  ❌ Error uploading rule: {e}")
            fail_count += 1
    
    logger.info(f"✅ {city_name}: {success_count} uploaded, {fail_count} failed")
    return success_count, fail_count

def main():
    """Load rules from JSON and upload to MCP"""
    
    # Check if MCP server is running
    try:
        response = requests.get(f"{MCP_API_BASE.replace('/api/mcp', '')}/")
        logger.info(f"✅ MCP Server is running: {response.json().get('message')}")
    except requests.exceptions.ConnectionError:
        logger.error("❌ MCP Server is not running! Start it with: python mcp_server.py")
        return
    
    # Load rules from JSON
    try:
        with open("mcp_data/rules.json", "r", encoding="utf-8") as f:
            all_rules = json.load(f)
    except FileNotFoundError:
        logger.error("❌ mcp_data/rules.json not found!")
        return
    
    # Upload each city
    total_success = 0
    total_fail = 0
    
    cities_to_upload = ["Pune", "Nashik"]  # Can add "Mumbai", "Ahmedabad" if needed
    
    for city in cities_to_upload:
        if city in all_rules:
            success, fail = upload_city_rules(city, all_rules[city])
            total_success += success
            total_fail += fail
        else:
            logger.warning(f"⚠️ {city} not found in rules.json")
    
    # Summary
    logger.info("=" * 50)
    logger.info(f"🎉 Upload Complete!")
    logger.info(f"   Total Uploaded: {total_success}")
    logger.info(f"   Total Failed: {total_fail}")
    logger.info("=" * 50)
    
    # Verify by listing all rules
    try:
        response = requests.get(f"{MCP_API_BASE}/list_rules?limit=50")
        if response.status_code == 200:
            data = response.json()
            logger.info(f"📊 Total rules in MCP database: {data.get('count', 0)}")
            
            # Count by city
            city_counts = {}
            for rule in data.get('rules', []):
                city = rule.get('city', 'Unknown')
                city_counts[city] = city_counts.get(city, 0) + 1
            
            logger.info("📍 Rules by city:")
            for city, count in city_counts.items():
                logger.info(f"   {city}: {count} rules")
    except Exception as e:
        logger.error(f"⚠️ Could not verify upload: {e}")

if __name__ == "__main__":
    main()

