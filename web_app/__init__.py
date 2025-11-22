# web_app/__init__.py
"""
Web application module containing:
- Flask app factory (create_app)
- Route bindings
- Templates & static assets
"""

from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    CORS(app)

    # Register routes
    from .routes import register_routes
    register_routes(app)

    return app
