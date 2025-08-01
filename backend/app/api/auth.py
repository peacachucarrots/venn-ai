from flask import Blueprint, request, current_app, abort, jsonify
from functools import wraps

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def auth_required(view):
    """Protect a view with the X-Admin-Token check"""
    @wraps(view)
    def wrapper(*args, **kwargs):
        token = request.headers.get("X-Admin-Token")
        if token != current_app.config["ADMIN_TOKEN"]:
            abort(401)
        return view(*args, **kwargs)
    return wrapper

@bp.route("/login", methods=["POST"])
def login():
    token = request.json.get("token")
    if token != current_app.config["ADMIN_TOKEN"]:
        abort(401)

    return jsonify({"status": "ok"})