# web_app/app.py
from flask import Flask, render_template, jsonify, request
from database.mongo_connection import get_db
from data_fetcher.config import PROCESSED_COLLECTION
import logging
from flask_cors import CORS

import threading
from run_pipeline import run_full_pipeline

def register_routes(app):
    ...
    @app.route("/admin/run_pipeline", methods=["POST"])
    def admin_run_pipeline():
        # start in background thread so request returns fast
        threading.Thread(target=run_full_pipeline, daemon=True).start()
        return jsonify({"status":"started"}), 200


app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)
logger = logging.getLogger(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/articles")
def api_articles():
    db = get_db()
    coll = db[PROCESSED_COLLECTION]
    limit = int(request.args.get("limit", 50))
    docs = list(coll.find().sort("processed_at", -1).limit(limit))
    for d in docs:
        d["_id"] = str(d["_id"])
    return jsonify(docs)

@app.route("/api/articles/category/<category>")
def api_by_category(category):
    db = get_db()
    coll = db[PROCESSED_COLLECTION]
    docs = list(coll.find({"category": category}).sort("processed_at", -1).limit(200))
    for d in docs:
        d["_id"] = str(d["_id"])
    return jsonify(docs)

@app.route("/dashboard")
def dashboard():
    return render_template("index.html")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True, host="0.0.0.0", port=5000)
