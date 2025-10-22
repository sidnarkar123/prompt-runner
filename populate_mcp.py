from utils import mcpstore
from samplerules import mumbairules, ahmedabadrules

def push_rules_to_mcp():
    print("📌 Populating MCP with Mumbai rules...")
    for r in mumbairules:
        meta = {"city": "Mumbai", "authority": r["authority"]}
        rule_id = mcpstore.save_rule(city="Mumbai", rule=r, meta=meta)
        print(f"Saved Mumbai rule {r['clause_no']} → ID: {rule_id}")
    print("\n📌 Populating MCP with Ahmedabad rules...")
    for r in ahmedabadrules:
        meta = {"city": "Ahmedabad", "authority": r["authority"]}
        rule_id = mcpstore.save_rule(city="Ahmedabad", rule=r, meta=meta)
        print(f"Saved Ahmedabad rule {r['clause_no']} → ID: {rule_id}")

if __name__ == "__main__":
    push_rules_to_mcp()
