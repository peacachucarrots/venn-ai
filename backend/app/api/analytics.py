from flask import Blueprint, jsonify
from sqlalchemy import func

from .auth import auth_required
from ..models.survey import Survey, SurveyVersion
from ..models.response import Response
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