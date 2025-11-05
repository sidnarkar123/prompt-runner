"""
Test script for Pune and Nashik city integration
"""
import json
import logging
from agents.agent_clients import get_rules_for_city
from agents.calculator_agent import calculator_agent
from utils.geometry_converter import json_to_glb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_city_rules(city_name: str):
    """Test fetching rules for a city"""
    logger.info(f"\n{'='*60}")
    logger.info(f"Testing {city_name} City Rules")
    logger.info(f"{'='*60}")
    
    rules = get_rules_for_city(city_name)
    
    if not rules:
        logger.warning(f"⚠️ No rules found for {city_name} in MCP!")
        logger.info(f"   💡 Run: python upload_cities_to_mcp.py")
        return False
    
    logger.info(f"✅ Found {len(rules)} rules for {city_name}")
    
    for i, rule in enumerate(rules, 1):
        logger.info(f"\n  Rule {i}: {rule.get('clause_no', 'N/A')}")
        logger.info(f"    Type: {rule.get('rule_type', 'N/A')}")
        logger.info(f"    Conditions: {rule.get('conditions', 'N/A')}")
        logger.info(f"    Entitlements: {rule.get('entitlements', 'N/A')}")
    
    return True

def test_calculator_agent(city_name: str):
    """Test calculator agent with city-specific rules"""
    logger.info(f"\n{'='*60}")
    logger.info(f"Testing Calculator Agent for {city_name}")
    logger.info(f"{'='*60}")
    
    # Test case: Residential building
    test_subject = {
        "height_m": 20,
        "fsi": 1.8,
        "setback_m": 3.5,
        "plot_area_sqm": 500
    }
    
    logger.info(f"Test Subject: {test_subject}")
    
    try:
        results = calculator_agent(city_name, test_subject)
        logger.info(f"✅ Calculator returned {len(results)} compliance checks")
        
        for i, result in enumerate(results[:3], 1):  # Show first 3
            logger.info(f"\n  Check {i} - Clause: {result.get('clause_no', 'N/A')}")
            checks = result.get('checks', {})
            for check_type, check_data in checks.items():
                status = "✅" if check_data.get('ok') else "❌"
                logger.info(f"    {status} {check_type}: {check_data}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Calculator agent failed: {e}")
        return False

def test_geometry_generation(city_name: str):
    """Test geometry generation for city"""
    logger.info(f"\n{'='*60}")
    logger.info(f"Testing Geometry Generation for {city_name}")
    logger.info(f"{'='*60}")
    
    # Create sample spec
    spec_data = {
        "city": city_name,
        "parameters": {
            "height_m": 21.0,
            "width_m": 25.0,
            "depth_m": 20.0,
            "setback_m": 3.5,
            "floor_height_m": 3.0,
            "fsi": 1.8,
            "type": "residential"
        },
        "status": "Compliant"
    }
    
    try:
        glb_path = json_to_glb(
            f"test_{city_name.lower()}.json",
            spec_data=spec_data
        )
        logger.info(f"✅ Generated GLB: {glb_path}")
        return True
    except Exception as e:
        logger.error(f"❌ Geometry generation failed: {e}")
        return False

def main():
    """Run all tests for Pune and Nashik"""
    
    cities = ["Pune", "Nashik"]
    
    print("\n" + "="*60)
    print("🧪 PUNE & NASHIK CITY INTEGRATION TESTS")
    print("="*60)
    
    results = {
        "rules": {},
        "calculator": {},
        "geometry": {}
    }
    
    for city in cities:
        results["rules"][city] = test_city_rules(city)
        results["calculator"][city] = test_calculator_agent(city)
        results["geometry"][city] = test_geometry_generation(city)
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for city in cities:
        print(f"\n{city}:")
        print(f"  Rules Fetch:       {'✅ PASS' if results['rules'][city] else '❌ FAIL'}")
        print(f"  Calculator Agent:  {'✅ PASS' if results['calculator'][city] else '❌ FAIL'}")
        print(f"  Geometry Gen:      {'✅ PASS' if results['geometry'][city] else '❌ FAIL'}")
    
    # Overall
    all_passed = all(
        results[test][city] 
        for test in results 
        for city in cities
    )
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️ SOME TESTS FAILED - Check logs above")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

