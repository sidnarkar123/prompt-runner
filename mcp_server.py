#mcp_server.py
from flask import Flask, request, jsonify
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- Mongo config (env-first) ---
MONGO_URI = os.environ.get(
    "MONGO_URI",
    os.environ.get("MONGO_URL", "mongodb://localhost:27017"),
)
MONGO_DB = os.environ.get("MONGO_DB", os.environ.get("MCP_DB", "mcp_database"))

# Create client with reasonable timeout
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
    client.admin.command("ping")
    logger.info("Connected to MongoDB (URI from env or default).")
except Exception as e:
    logger.exception("Cannot connect to MongoDB. Check MONGO_URI and network: %s", e)
    raise SystemExit(1)

db = client[MONGO_DB]

# --- Collections ---
rules_col = db.get_collection("rules")
feedback_col = db.get_collection("feedback")
geometry_col = db.get_collection("geometry_outputs")
documents_col = db.get_collection("documents")
rl_logs_col = db.get_collection("rl_logs")


# === API: Save Rule (POST) ===
@app.route("/api/mcp/save_rule", methods=["POST"])
def save_rule():
    try:
        payload = request.get_json(force=True)
        if not payload:
            return jsonify({"success": False, "error": "No JSON body"}), 400

        if isinstance(payload, dict) and "rules" in payload and isinstance(payload["rules"], list):
            doc_record = {
                "filename": payload.get("source_file"),
                "city": payload.get("city"),
                "parsed_at": payload.get("parsed_at", datetime.utcnow().isoformat() + "Z"),
                "rule_count": payload.get("rule_count", len(payload.get("rules", []))),
                "raw": payload,
            }
            dres = documents_col.insert_one(doc_record)
            doc_id = str(dres.inserted_id)
            inserted_ids = []
            for r in payload["rules"]:
                rule_record = {
                    "city": payload.get("city"),
                    "clause_no": r.get("clause_no"),
                    "summary": r.get("summary"),
                    "full_text": r.get("full_text"),
                    "source_doc_id": doc_id,
                    "inserted_at": datetime.utcnow().isoformat() + "Z",
                }
                rr = rules_col.insert_one(rule_record)
                inserted_ids.append(str(rr.inserted_id))
            return jsonify({"success": True, "document_id": doc_id, "inserted_rules": inserted_ids}), 201

        rule = payload
        rule_record = {
            "city": rule.get("city"),
            "authority": rule.get("authority"),
            "clause_no": rule.get("clause_no") or rule.get("id"),
            "page": rule.get("page"),
            "rule_type": rule.get("rule_type"),
            "conditions": rule.get("conditions") or rule.get("summary") or rule.get("full_text"),
            "entitlements": rule.get("entitlements"),
            "notes": rule.get("notes"),
            "created_at": datetime.utcnow().isoformat() + "Z",
        }
        res = rules_col.insert_one(rule_record)
        return jsonify({"success": True, "inserted_id": str(res.inserted_id)}), 201

    except Exception as e:
        logger.exception("Error in save_rule: %s", e)
        return jsonify({"success": False, "error": str(e)}), 500


# === API: List All Rules (GET) ===
@app.route("/api/mcp/list_rules", methods=["GET"])
def list_rules():
    try:
        limit = int(request.args.get("limit", 100))
        rules = list(rules_col.find({}, {"_id": 0}).limit(limit))
        return jsonify({"success": True, "count": len(rules), "rules": rules}), 200
    except Exception as e:
        logger.exception("Error in list_rules: %s", e)
        return jsonify({"success": False, "error": str(e)}), 500


# === API: Delete Rule by ID (DELETE) ===
@app.route("/api/mcp/delete_rule/<rule_id>", methods=["DELETE"])
def delete_rule(rule_id):
    try:
        from bson.objectid import ObjectId
        try:
            res = rules_col.delete_one({"_id": ObjectId(rule_id)})
        except Exception:
            res = rules_col.delete_one({"id": rule_id})
        if res.deleted_count == 0:
            return jsonify({"success": False, "message": "No rule deleted"}), 404
        return jsonify({"success": True, "deleted_count": res.deleted_count}), 200
    except Exception as e:
        logger.exception("Error in delete_rule: %s", e)
        return jsonify({"success": False, "error": str(e)}), 500


# === API: Save Feedback (POST) ===
@app.route("/api/mcp/feedback", methods=["POST"])
def save_feedback():
    try:
        payload = request.get_json(force=True)
        if not payload:
            return jsonify({"success": False, "error": "Empty payload"}), 400

        case_id = payload.get("case_id")
        fb = payload.get("feedback")
        if not case_id or fb not in ("up", "down"):
            return jsonify({"success": False, "error": "Missing or invalid 'case_id' or 'feedback'"}), 400

        score = 2 if fb == "up" else -2
        entry = {
            "case_id": case_id,
            "input": payload.get("input"),
            "output": payload.get("output"),
            "user_feedback": fb,
            "score": score,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        fres = feedback_col.insert_one(entry)

        rl_entry = {
            "case_id": case_id,
            "reward": score,
            "source": "user_feedback",
            "details": {"feedback_id": str(fres.inserted_id)},
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        rl_logs_col.insert_one(rl_entry)

        logger.info("Saved feedback for %s -> %s (score=%s)", case_id, fb, score)
        return jsonify({"success": True, "feedback_id": str(fres.inserted_id), "reward": score}), 201

    except Exception as e:
        logger.exception("Error in save_feedback: %s", e)
        return jsonify({"success": False, "error": str(e)}), 500


# === API: Save Geometry Reference (POST) ===
@app.route("/api/mcp/geometry", methods=["POST"])
def save_geometry():
    try:
        payload = request.get_json(force=True)
        if not payload:
            return jsonify({"success": False, "error": "Empty payload"}), 400
        case_id = payload.get("case_id")
        file_path = payload.get("file")
        if not case_id or not file_path:
            return jsonify({"success": False, "error": "Missing 'case_id' or 'file'"}), 400

        geometry_col.update_one(
            {"case_id": case_id},
            {
                "$set": {
                    "file": file_path,
                    "metadata": payload.get("metadata", {}),
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                }
            },
            upsert=True,
        )
        logger.info("Saved geometry for case %s -> %s", case_id, file_path)
        return jsonify({"success": True, "case_id": case_id, "file": file_path}), 201

    except Exception as e:
        logger.exception("Error in save_geometry: %s", e)
        return jsonify({"success": False, "error": str(e)}), 500


# === Root endpoint ===
@app.route("/", methods=["GET"])
def index():
    return jsonify(
        {
            "message": "MCP API running",
            "db": MONGO_DB,
            "endpoints": [
                "POST /api/mcp/save_rule",
                "GET /api/mcp/list_rules",
                "DELETE /api/mcp/delete_rule/<rule_id>",
                "POST /api/mcp/feedback",
                "POST /api/mcp/geometry",
            ],
        }
    ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
# ...existing code...