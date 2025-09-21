from flask import Blueprint, jsonify, make_response, request
from uuid import UUID
from sqlalchemy.dialects.postgresql import insert
from ..models.visitor import Visitor
from ..extensions import db

bp = Blueprint('visitors', __name__, url_prefix='/api/visitors')

def ensure_visitor(visitor_id: str | None) -> str:
    if visitor_id:
        try:
            UUID(visitor_id)
        except ValueError:
            visitor_id = None

    if visitor_id:
        stmt = insert(Visitor).values(visitor_id=visitor_id).on_conflict_do_nothing(
            index_elements=[Visitor.visitor_id]
        )
        db.session.execute(stmt)
        db.session.commit()
        return visitor_id

    v = Visitor()
    db.session.add(v)
    db.session.commit()
    return str(v.visitor_id)

@bp.post("/")
def create_visitor():
    cookie_id = request.cookies.get("visitor_id")
    vid = ensure_visitor(cookie_id)

    response = make_response(jsonify({"visitor_id": vid}), 201 if cookie_id is None else 200)
    response.set_cookie(
        key="visitor_id",
        value=vid,
        max_age=60 * 60 * 24 * 365,
        httponly=True,
        samesite="lax"
    )
    return response
