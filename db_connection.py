# db_connection.py
import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_db():
    try:
        MONGO_URI = os.getenv("MONGO_URI")
        MONGO_DB = os.getenv("MONGO_DB", "mcp_database")

        client = MongoClient(
            MONGO_URI,
            tls=True,
            tlsCAFile=certifi.where(),  # ✅ Trusted CA certificates
            serverSelectionTimeoutMS=20000
        )

        db = client[MONGO_DB]
        client.admin.command('ping')  # ✅ Forces handshake test
        print(f"✅ Connected to MongoDB: {db.name}")
        return db

    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return None

# Test
if __name__ == "__main__":
    get_db()
