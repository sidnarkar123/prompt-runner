from flask import Flask, request, jsonify
from datetime import datetime
from pymongo import MongoClient
from urllib.parse import quote_plus
import os

app = Flask(__name__)

# === MongoDB Atlas Connection ===
username = "siddhesh001"
password = quote_plus("siddhesh@123")  # <-- safely encode special characters
MONGO_URI = f"mongodb+srv://{username}:{password}@cluster0.yzses0a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client["mcp_database"]

# === Collections ===
rules_col = db["rules"]
feedback_col = db["feedback"]
geometry_col = db["geometry"]

# === API: Save Rule (POST) ===
@app.route("/api/mcp/save_rule", methods=["POST"])
def save_rule():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"success": False, "error": "No JSON data received"}), 400

        city = data.get("city", "unknown")
        rule_id = data.get("id") or os.urandom(4).hex()

        record = {
            "id": rule_id,
            "city": city,
            "rule": data.get("rule", data),
            "meta": {k: data[k] for k in data if k not in ["rule", "id"]},
            "time": datetime.utcnow().isoformat() + "Z"
        }

        rules_col.insert_one(record)
        print(f"✅ [SAVE] New rule saved for city '{city}' → id: {rule_id}")

        return jsonify({"success": True, "message": "Rule saved successfully", "id": rule_id}), 201
    except Exception as e:
        print(f"❌ [ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# === API: List All Rules (GET) ===
@app.route("/api/mcp/list_rules", methods=["GET"])
def list_rules():
    try:
        all_rules = list(rules_col.find({}, {"_id": 0}))
        return jsonify({"success": True, "count": len(all_rules), "rules": all_rules}), 200
    except Exception as e:
        print(f"❌ [ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# === API: Delete Rule by ID (DELETE) ===
@app.route("/api/mcp/delete_rule/<rule_id>", methods=["DELETE"])
def delete_rule(rule_id):
    try:
        result = rules_col.delete_one({"id": rule_id})
        if result.deleted_count == 0:
            return jsonify({"success": False, "error": "Rule ID not found"}), 404

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

        reward = 2 if fb == "up" else -2
        entry = {
            "case_id": case_id,
            "feedback": fb,
            "reward": reward,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        feedback_col.insert_one(entry)
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

        geometry_col.update_one(
            {"case_id": case_id},
            {"$set": {"file": file_path, "timestamp": datetime.utcnow().isoformat() + "Z"}},
            upsert=True
        )

        print(f"💾 [GEOMETRY] Saved geometry for case {case_id}: {file_path}")
        return jsonify({"success": True, "stored": data}), 201
    except Exception as e:
        print(f"❌ [ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# === Root endpoint ===
@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "✅ MCP Rule API (MongoDB Atlas) is running",
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
