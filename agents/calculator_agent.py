from agent_clients import get_rules, log_geometry

def calculator_agent(city):
    """
    Fetch rules from MCP API, perform dummy computation,
    log geometry paths.

    Returns computed output list for validation.
    """
    rules = get_rules(city)
    outputs = []
    for r in rules:
        rule_data = r["rule"]
        entitle = "Allowed" if "height" in rule_data.get("conditions", "").lower() else "Check"
        outputs.append({
            "clause_no": rule_data.get("clause_no", ""),
            "entitlement": entitle
        })
        log_geometry(r["id"], f"outputs/geometry/{r['id']}.glb")
    return outputs
