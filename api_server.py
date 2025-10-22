from flask import Flask, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

# === MCP Data Folder Setup ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MCP_DIR = os.path.join(BASE_DIR, "mcpdata")
os.makedirs(MCP_DIR, exist_ok=True)

RULES_FILE = os.path.join(MCP_DIR, "rules.json")
FEEDBACK_FILE = os.path.join(MCP_DIR, "feedback.json")
GEOMETRY_FILE = os.path.join(MCP_DIR, "geometry.json")

# === Helper Functions to Read/Write JSON ===
def _read_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# === API: Save Rule (POST) ===
@app.route("/api/mcp/save_rule", methods=["POST"])
def save_rule():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"success": False, "error": "No JSON data received"}), 400

        city = data.get("city", "unknown")
        rules = _read_json(RULES_FILE)
        if city not in rules:
            rules[city] = []

        rule_id = data.get("id") or os.urandom(4).hex()
        rec = {
            "id": rule_id,
            "rule": data.get("rule", data),
            "meta": {k: data[k] for k in data if k not in ["rule", "id"]},
            "time": datetime.utcnow().isoformat() + "Z"
        }
        rules[city].append(rec)
        _write_json(RULES_FILE, rules)

        print(f"✅ [SAVE] New rule saved for city '{city}' → id: {rule_id}")
        return jsonify({"success": True, "message": "Rule saved successfully", "id": rule_id}), 201
    except Exception as e:
        print(f"❌ [ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# === API: List All Rules (GET) ===
@app.route("/api/mcp/list_rules", methods=["GET"])
def list_rules():
    try:
        rules = _read_json(RULES_FILE)
        all_rules = []
        for city, recs in rules.items():
            for r in recs:
                all_rules.append({
                    "city": city,
                    "id": r.get("id"),
                    "rule": r.get("rule"),
                    "meta": r.get("meta"),
                    "time": r.get("time")
                })
        return jsonify({"success": True, "count": len(all_rules), "rules": all_rules}), 200
    except Exception as e:
        print(f"❌ [ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# === API: Delete Rule by ID (DELETE) ===
@app.route("/api/mcp/delete_rule/<rule_id>", methods=["DELETE"])
def delete_rule(rule_id):
    try:
        rules = _read_json(RULES_FILE)
        found = False
        for city, recs in rules.items():
            for r in recs:
                if r.get("id") == rule_id:
                    recs.remove(r)
                    found = True
                    break
            if found:
                break

        if not found:
            return jsonify({"success": False, "error": "Rule ID not found"}), 404

        _write_json(RULES_FILE, rules)
        print(f"🗑️ [DELETE] Rule deleted → {rule_id}")
        return jsonify({"success": True, "message": f"Rule {rule_id} deleted"}), 200
    except Exception as e:
        print(f"❌ [ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# === API: Save Feedback (POST) ===
@app.route("/api/mcp/feedback", methods=["POST"])
def save_feedback():
    try:
        data = request.get_json(force=True)
        case_id = data.get("case_id")
        fb = data.get("feedback")
        if case_id is None or fb not in ["up", "down"]:
            return jsonify({"success": False, "error": "Invalid feedback data"}), 400

        db = _read_json(FEEDBACK_FILE)
        reward = 2 if fb == "up" else -2

        entry = {
            "case_id": case_id,
            "feedback": fb,
            "reward": reward,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        db.setdefault(case_id, []).append(entry)
        _write_json(FEEDBACK_FILE, db)

        print(f"💾 [FEEDBACK] {case_id} → {fb} (reward={reward})")
        return jsonify({"success": True, "reward": reward}), 201
    except Exception as e:
        print(f"❌ [ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# === API: Save Geometry Reference (POST) ===
@app.route("/api/mcp/geometry", methods=["POST"])
def save_geometry():
    try:
        data = request.get_json(force=True)
        case_id = data.get("case_id")
        file_path = data.get("file")
        if not case_id or not file_path:
            return jsonify({"success": False, "error": "Missing 'case_id' or 'file' path"}), 400

        db = _read_json(GEOMETRY_FILE)
        db[case_id] = {
            "file": file_path,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        _write_json(GEOMETRY_FILE, db)

        print(f"💾 [GEOMETRY] Saved geometry for case {case_id}: {file_path}")
        return jsonify({"success": True, "stored": data}), 201
    except Exception as e:
        print(f"❌ [ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# === Root endpoint ===
@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "MCP Rule API is running",
        "endpoints": {
            "POST /api/mcp/save_rule": "Save new rule JSON",
            "GET /api/mcp/list_rules": "List all saved rules",
            "DELETE /api/mcp/delete_rule/<rule_id>": "Delete a rule by ID",
            "POST /api/mcp/feedback": "Save user feedback",
            "POST /api/mcp/geometry": "Save geometry reference"
        }
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
