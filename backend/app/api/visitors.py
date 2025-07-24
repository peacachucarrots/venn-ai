from flask import Blueprint, jsonify, make_response
from ..models.visitor import Visitor
from ..extensions import db

bp = Blueprint('visitors', __name__, url_prefix='/api/visitors')

@bp.post("/")
def create_visitor():
    v = Visitor()
    db.session.add(v)
    db.session.commit()

    r = make_response(jsonify({"visitor_id": str(v.visitor_id)}), 201)
    r.set_cookie(
        key="visitor_id",
        value=str(v.visitor_id),
        max_age=60 * 60 * 24 * 365,
        httponly=True,
        samesite="lax"
    )
    return r
