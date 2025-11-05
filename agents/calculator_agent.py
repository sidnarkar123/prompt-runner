# agents/calculator_agent.py
import logging
import re
from typing import List, Dict, Any
from agents.agent_clients import get_rules_for_city, log_geometry
from utils.geometry_converter import json_to_glb
import os
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)

# Helper: evaluate a simple numeric constraint (height)
def _evaluate_height_condition(parsed_height, subject_height_m: float) -> bool:
    if not parsed_height:
        return False
    op = parsed_height.get("op")
    val = parsed_height.get("value_m")
    if op == "<=":
        return subject_height_m <= val
    if op == "<":
        return subject_height_m < val
    if op == ">=":
        return subject_height_m >= val
    if op == ">":
        return subject_height_m > val
    if op == "=":
        return subject_height_m == val
    return False

def calculator_agent(city: str, subject: Dict[str, Any]) -> List[Dict[str,Any]]:
    """
    subject: dict with properties to check, e.g. {"height_m": 20, "fsi": 2.2}
    Returns outputs and logs geometry file references in MCP.
    """
    rules = get_rules_for_city(city)
    outputs = []

    for r in rules:
        rule_obj = r.get("rule", r)  # some endpoints return wrapped
        parsed = rule_obj.get("parsed_fields") or rule_obj.get("parsed") or {}
        height_rule = parsed.get("height")
        fsi_rule = parsed.get("fsi") or parsed.get("fsi")

        outcome = {"id": r.get("id"), "clause_no": rule_obj.get("clause_no"), "checks": {}}

        # Height check
        if "height_m" in subject and height_rule:
            ok = _evaluate_height_condition(height_rule, float(subject["height_m"]))
            outcome["checks"]["height"] = {"ok": ok, "rule": height_rule, "subject": subject["height_m"]}
        else:
            outcome["checks"]["height"] = {"ok": None, "rule": height_rule, "subject": subject.get("height_m")}

        # FSI check
        if "fsi" in subject and fsi_rule:
            try:
                val = float(fsi_rule)
                outcome["checks"]["fsi"] = {"ok": subject["fsi"] <= val, "rule": val, "subject": subject["fsi"]}
            except Exception:
                outcome["checks"]["fsi"] = {"ok": None, "rule": fsi_rule, "subject": subject.get("fsi")}
        else:
            outcome["checks"]["fsi"] = {"ok": None, "rule": fsi_rule, "subject": subject.get("fsi")}

        outputs.append(outcome)

        # Create realistic 3D geometry from the rule and subject data
        case_id = r.get("id") or (rule_obj.get("clause_no") or "unknown")
        
        # Build spec data for geometry generation
        geometry_spec = {
            "parameters": {
                "height_m": subject.get("height_m", 20),
                "width_m": subject.get("width_m", 30),
                "depth_m": subject.get("depth_m", 20),
                "setback_m": subject.get("setback_m", 3),
                "floor_height_m": subject.get("floor_height_m", 3),
                "type": subject.get("type", "residential"),
                "fsi": subject.get("fsi")
            },
            "status": "compliant" if all(c.get("ok") for c in outcome["checks"].values() if c.get("ok") is not None) else "non-compliant"
        }
        
        # Generate GLB using improved converter
        try:
            geom_path = json_to_glb(
                json_path=f"{case_id}.json",  # Just for naming
                output_dir="outputs/geometry",
                spec_data=geometry_spec
            )
            log_geometry(case_id, geom_path)
            logging.info(f"✅ Generated 3D geometry for {case_id}: {geom_path}")
        except Exception as e:
            logging.error(f"Failed to generate geometry for {case_id}: {e}")

    # also write a local output summary
    summary_path = f"outputs/{city}_calc_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.json"
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(outputs, f, indent=2)

    logging.info("Calculator finished for %s -> %d outcomes", city, len(outputs))
    return outputs
