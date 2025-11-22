# web_app/routes.py
from flask import render_template, jsonify, request
from database.mongo_connection import get_db
from config.settings import PROCESSED_COLLECTION
import logging

logger = logging.getLogger(__name__)

def register_routes(app):

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/category/<cat>")
    def category(cat):
        return render_template("category.html", category=cat)

    @app.route("/api/articles")
    def api_all():
        limit = int(request.args.get("limit", 50))
        db = get_db()
        docs = list(db[PROCESSED_COLLECTION].find().sort("processed_at", -1).limit(limit))

        for d in docs:
            d["_id"] = str(d["_id"])
        return jsonify(docs)

    @app.route("/api/articles/category/<cat>")
    def api_category(cat):
        db = get_db()
        docs = list(db[PROCESSED_COLLECTION].find({"category": cat}).sort("processed_at", -1).limit(200))

        for d in docs:
            d["_id"] = str(d["_id"])
        return jsonify(docs)
