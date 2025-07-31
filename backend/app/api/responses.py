from flask import Blueprint, jsonify, request, abort, current_app
from datetime import datetime, timezone
import json
from ..extensions import db
from ..models.response import Response, Answer
from ..models.survey import Question, QuestionType, SurveyVersion
from ..models.visitor import Visitor
from ..services.analysis_service import analyze_response

bp = Blueprint('responses', __name__, url_prefix='/api/responses')

@bp.post("/create-response")
def create_response():
    # check to make sure all data is accurate and exists
    data = request.get_json()
    if not data:
        abort(400, "Unexpected/Invalid JSON format (or missing JSON?)")

    svid = data.get("survey_version_id")
    if not svid:
        abort(400, "survey_version_id missing")

    version = SurveyVersion.query.get_or_404(svid)

    visitor_id = request.cookies.get("visitor_id")
    if visitor_id is None:
        abort(400, "Missing visitor cookie")

    resp = Response(survey_version_id=version.survey_version_id, visitor_id=visitor_id)
    db.session.add(resp)
    db.session.flush()

    for a in data["answers"]:
        q = Question.query.get(a["question_id"])
        if q.question_type == QuestionType.contact:
            value = a.get("text")
            if value is None:
                continue

            visitor = Visitor.query.get(visitor_id) or Visitor(visitor_id=visitor_id)

            prompt = q.prompt.lower()
            current_app.logger.debug(prompt)
            if prompt == "first name":
                visitor.first_name = value
            elif prompt == "last name":
                visitor.last_name = value
            elif prompt == "email":
                visitor.email = value
            elif prompt == "phone number":
                visitor.phone = value
            elif prompt == "company":
                visitor.company = value
            db.session.add(visitor)
        else:
            db.session.add(
                Answer(
                    response_id=resp.response_id,
                    question_id=a["question_id"],
                    option_id=a["option_id"],
                )
            )
    db.session.flush()

    analysis = analyze_response(resp)
    resp.analysis = analysis
    resp.submitted_at = datetime.now(timezone.utc)
    db.session.commit()

    # return parsed analysis
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
        "survey_version_id": str(resp.survey_version_id),
        "visitor_id": str(resp.visitor_id),
        "submitted_at": resp.submitted_at.isoformat(),
        "answers": answers,
        "analysis": resp.analysis,
    })