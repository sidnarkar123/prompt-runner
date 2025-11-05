#!/usr/bin/env python3
"""
Test multi-city support (Mumbai, Ahmedabad, Pune, Nashik)
"""
import json
from agents.agent_clients import get_rules_for_city
from agents.calculator_agent import calculator_agent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_city_rules(city: str):
    """Test if rules are available for a city"""
    logger.info(f"\n{'='*60}")
    logger.info(f"🏙️  Testing: {city}")
    logger.info(f"{'='*60}")
    
    rules = get_rules_for_city(city)
    
    if not rules:
        logger.warning(f"⚠️  No rules found for {city}")
        logger.warning(f"   Run: python upload_all_cities.py")
        return False
    
    logger.info(f"✅ Found {len(rules)} rules for {city}")
    
    # Show rule types
    rule_types = {}
    for rule in rules:
        rule_obj = rule.get("rule", rule)
        rule_type = rule_obj.get("rule_type", "Unknown")
        rule_types[rule_type] = rule_types.get(rule_type, 0) + 1
    
    logger.info(f"\n📊 Rule Types:")
    for rtype, count in sorted(rule_types.items()):
        logger.info(f"   {rtype}: {count}")
    
    # Show sample rules
    logger.info(f"\n📄 Sample Rules:")
    for i, rule in enumerate(rules[:3], 1):
        rule_obj = rule.get("rule", rule)
        clause = rule_obj.get("clause_no", "N/A")
        conditions = rule_obj.get("conditions", "N/A")
        logger.info(f"   {i}. {clause}: {conditions}")
    
    return True


def test_calculator_with_city(city: str):
    """Test calculator agent with a city"""
    logger.info(f"\n🧮 Testing Calculator Agent for {city}")
    
    # Sample building subject for testing
    test_subjects = {
        "Mumbai": {"height_m": 20, "fsi": 2.0, "width_m": 30, "depth_m": 20, "type": "residential"},
        "Ahmedabad": {"height_m": 15, "fsi": 1.5, "width_m": 25, "depth_m": 18, "type": "residential"},
        "Pune": {"height_m": 18, "fsi": 1.8, "width_m": 28, "depth_m": 20, "type": "commercial"},
        "Nashik": {"height_m": 16, "fsi": 1.6, "width_m": 24, "depth_m": 16, "type": "residential"}
    }
    
    subject = test_subjects.get(city, {"height_m": 20, "fsi": 2.0})
    
    try:
        results = calculator_agent(city, subject)
        logger.info(f"   ✅ Calculator returned {len(results)} outcomes")
        
        # Show compliance summary
        compliant = sum(1 for r in results if all(
            check.get("ok") for check in r.get("checks", {}).values() 
            if check.get("ok") is not None
        ))
        logger.info(f"   📊 {compliant}/{len(results)} rules passed")
        
        return True
    except Exception as e:
        logger.error(f"   ❌ Calculator failed: {e}")
        return False


def main():
    """Test all cities"""
    cities = ["Mumbai", "Ahmedabad", "Pune", "Nashik"]
    
    logger.info("🚀 Multi-City Compliance System Test\n")
    
    results = {}
    
    # Test 1: Check rules availability
    logger.info("\n" + "="*60)
    logger.info("TEST 1: Rules Availability")
    logger.info("="*60)
    
    for city in cities:
        results[city] = {"rules": test_city_rules(city)}
    
    # Test 2: Calculator agent integration
    logger.info("\n" + "="*60)
    logger.info("TEST 2: Calculator Agent Integration")
    logger.info("="*60)
    
    for city in cities:
        if results[city]["rules"]:
            results[city]["calculator"] = test_calculator_with_city(city)
        else:
            logger.info(f"\n⏭️  Skipping {city} calculator test (no rules)")
            results[city]["calculator"] = False
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("📊 TEST SUMMARY")
    logger.info("="*60)
    
    for city in cities:
        rules_status = "✅" if results[city].get("rules") else "❌"
        calc_status = "✅" if results[city].get("calculator") else "❌"
        logger.info(f"{city:12} | Rules: {rules_status} | Calculator: {calc_status}")
    
    # Overall status
    all_passed = all(
        results[city].get("rules") and results[city].get("calculator")
        for city in cities
    )
    
    logger.info("\n" + "="*60)
    if all_passed:
        logger.info("✅ All tests PASSED! Multi-city system is working.")
    else:
        logger.warning("⚠️ Some tests FAILED. Check logs above.")
        logger.info("\n💡 If rules are missing, run:")
        logger.info("   python upload_all_cities.py")
    logger.info("="*60 + "\n")


if __name__ == "__main__":
    main()

