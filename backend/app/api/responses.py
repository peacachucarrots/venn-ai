from flask import Blueprint, jsonify, request, abort
from datetime import datetime, timezone
import uuid, json
from ..extensions import db
from ..models.response import Response, Answer
from ..models.survey import Question, QuestionType
from ..models.visitor import Visitor
from ..services.analysis_service import analyze_response

bp = Blueprint('responses', __name__, url_prefix='/api/responses')

@bp.post("/create-response")
def create_response():
    survey_id = uuid.UUID("810056b0-b8ad-4f6e-ac45-4ba3f864aa2b")
    if survey_id is None:
        abort(400, "Missing survey id")

    visitor_id = request.cookies.get("visitor_id")
    if visitor_id is None:
        abort(400, "Missing visitor cookie")

    data = request.get_json()
    resp = Response(survey_id=survey_id, visitor_id=visitor_id)
    db.session.add(resp)
    db.session.flush()

    for a in data["answers"]:
        q = Question.query.get(a["question_id"])
        if q.question_type == QuestionType.contact:
            contact = a["answer"]
            visitor = Visitor.query.get(visitor_id) or Visitor(visitor_id=visitor_id)
            visitor.first_name = contact.get("first_name")
            visitor.last_name = contact.get("last_name")
            visitor.email = contact.get("email")
            visitor.phone = contact.get("phone_number")
            visitor.company = contact.get("company")
            db.session.add(visitor)
        else:
            db.session.add(
                Answer(
                    response_id=resp.response_id,
                    question_id=a["question_id"],
                    option_id=a["option_id"],
                )
            )
    db.session.commit()

    analysis = analyze_response(resp)
    resp.analysis = analysis
    resp.submitted_at = datetime.now(timezone.utc)
    db.session.commit()

    parsed = json.loads(analysis)

    return jsonify({
        "response_id": str(resp.response_id),
        "analysis": parsed
    })

@bp.get("/<uuid:response_id>")
def get_response(response_id):
    resp = Response.query.get(response_id)
    if not resp:
        abort(404, f"No response with id {response_id}")

    answers = [
        {
            "question_id": ans.question_id,
            "option_id": ans.option_id
        }
        for ans in resp.answers
    ]

    return jsonify({
        "response_id": str(resp.response_id),
        "survey_id": str(resp.survey_id),
        "visitor_id": str(resp.visitor_id),
        "submitted_at": resp.submitted_at.isoformat(),
        "answers": answers,
        "analysis": resp.analysis,
    })