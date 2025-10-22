from utils import mcp_store
import json

# Check Mumbai rules
mumbai_rules = mcp_store.get_rules("Mumbai")
print(f"Mumbai rules count: {len(mumbai_rules)}")
print(json.dumps(mumbai_rules, indent=2))

# Check Ahmedabad rules
ahmedabad_rules = mcp_store.get_rules("Ahmedabad")
print(f"Ahmedabad rules count: {len(ahmedabad_rules)}")
print(json.dumps(ahmedabad_rules, indent=2))
