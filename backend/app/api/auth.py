from flask import Blueprint, request, current_app, abort, jsonify

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route("/login", methods=["POST"])
def login():
    token = request.json.get("token")
    if token != current_app.config["ADMIN_TOKEN"]:
        abort(401)

    return jsonify({"status": "ok"})