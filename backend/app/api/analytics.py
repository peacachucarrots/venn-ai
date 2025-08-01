from flask import Blueprint, jsonify, abort
from sqlalchemy import func

from .auth import auth_required
from ..models.survey import Survey, SurveyVersion, Question, Option
from ..models.response import Response, Answer
from ..models.visitor import Visitor
from ..extensions import db

bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

@bp.route("/overview")
@auth_required
def overview():
    total_surveys = db.session.scalar(func.count(Survey.survey_id))
    active_surveys = (
        db.session.query(Survey)
        .join(Survey.versions)
        .filter(SurveyVersion.is_active.is_(True))
        .distinct()
        .count()
    )
    total_responses = db.session.scalar(func.count(Response.response_id))
    unique_visitors = db.session.scalar(func.count(Visitor.visitor_id))

    return jsonify(
        total_surveys=total_surveys,
        active_surveys=active_surveys,
        total_responses=total_responses,
        unique_visitors=unique_visitors
    )

@bp.route("/surveys")
@auth_required
def surveys_summary():
    rows = (
        db.session.query(
            Survey.survey_id,
            Survey.name,
            func.count(Response.response_id).label("response_count"),
        )
        .join(SurveyVersion, SurveyVersion.survey_id == Survey.survey_id)
        .filter(SurveyVersion.is_active.is_(True))
        .outerjoin(Response, Response.survey_version_id == SurveyVersion.survey_version_id)
        .group_by(Survey.survey_id, Survey.name)
        .order_by(func.count(Response.response_id).desc())
        .all()
    )
    return jsonify([
        {
            "survey_id": str(r.survey_id),
            "name": r.name,
            "responses": r.response_count
        }
        for r in rows
    ])

@bp.route("/survey/<uuid:survey_id>/responses")
@auth_required
def survey_responses(survey_id):
    versions = (
        db.session.query(SurveyVersion)
        .filter(SurveyVersion.survey_id == survey_id)
        .order_by(SurveyVersion.revision.desc())
        .all()
    )
    if not versions:
        abort(404, description="No versions found for this survey ID")

    version_ids = [v.survey_version_id for v in versions]
    rev_by_id = {v.survey_version_id: v.revision for v in versions}

    questions = (
        db.session.query(Question, SurveyVersion.revision)
        .join(SurveyVersion, SurveyVersion.survey_version_id == Question.survey_version_id)
        .filter(Question.survey_version_id.in_(version_ids))
        .order_by(SurveyVersion.revision.desc(), Question.order_number)
        .all()
    )

    question_cols = [
        {
            "id": str(q.question_id),
            "prompt": q.prompt,
            "revision": rev
        }
        for(q, rev) in questions
    ]

    rows = (
        db.session.query(
            Response.response_id,
            Response.submitted_at,
            Response.survey_version_id,
            Visitor.first_name,
            Visitor.last_name,
            Visitor.email,
            Answer.question_id,
            Option.label,
            Answer.free_text,
            Answer.numeric_value
        )
        .join(Visitor, Visitor.visitor_id == Response.visitor_id)
        .join(Answer, Answer.response_id == Response.response_id)
        .outerjoin(Option, Option.option_id == Answer.option_id)
        .filter(Response.survey_version_id.in_(version_ids))
        .order_by(Response.submitted_at.desc())
        .all()
    )

    resp_map = {}
    for r in rows:
        entry = resp_map.setdefault(r.response_id, {
            "submitted_at": r.submitted_at.isoformat(timespec="seconds"),
            "revision": rev_by_id.get(r.survey_version_id, None),
            "name": f"{(r.first_name or '').strip()} {(r.last_name or '').strip()}",
            "email": r.email or "-",
            "answers": {}
        })

        if r.label is not None:
            val = r.label
        elif r.free_text:
            val = r.free_text
        elif r.numeric_value is not None:
            val = float(r.numeric_value)
        else:
            val = "-"
        entry["answers"][str(r.question_id)] = val

    return jsonify({
        "questions": question_cols,
        "responses": list(resp_map.values())
    })