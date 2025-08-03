from collections import OrderedDict

from flask import Blueprint, jsonify, abort
from sqlalchemy import func, select, distinct

from .helpers.helper import _norm_prompt

from ...api.auth import auth_required
from ...models.survey import Survey, SurveyVersion, Question, Option
from ...models.response import Response, Answer
from ...models.visitor import Visitor
from ...extensions import db

bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

@bp.route("/overview")
@auth_required
def overview():
    total_surveys = db.session.scalar(select(func.count()).select_from(Survey))
    total_versions = db.session.scalar(select(func.count()).select_from(SurveyVersion))

    active_surveys = db.session.scalar(
        select(func.count(distinct(Survey.survey_id)))
        .select_from(Survey)
        .join(SurveyVersion, SurveyVersion.survey_id == Survey.survey_id)
        .where(SurveyVersion.is_active.is_(True))
    )

    total_responses = db.session.scalar(select(func.count()).select_from(Response))
    unique_visitors = db.session.scalar(select(func.count()).select_from(Visitor))

    return jsonify(
        total_surveys=total_surveys,
        total_versions=total_versions,
        active_surveys=active_surveys,
        total_responses=total_responses,
        unique_visitors=unique_visitors
    )

@bp.route("/surveys")
@auth_required
def surveys_summary():
    all_resp_count = func.count(distinct(Response.response_id))
    active_resp_count = (
        func.count(distinct(Response.response_id))
        .filter(SurveyVersion.is_active.is_(True))
    )

    rows = (
        db.session.query(
            Survey.survey_id,
            Survey.name,
            all_resp_count.label("responses_all"),
            active_resp_count.label("responses_active")
        )
        .outerjoin(SurveyVersion, SurveyVersion.survey_id == Survey.survey_id)
        .outerjoin(Response, Response.survey_version_id == SurveyVersion.survey_version_id)
        .group_by(Survey.survey_id, Survey.name)
        .order_by(all_resp_count.desc())
        .all()
    )

    return jsonify([
        {
            "survey_id": str(r.survey_id),
            "name": r.name,
            "responses": r.responses_all,
            "responses_active": r.responses_active
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

    qrows = (
        db.session.query(
            Question.question_id,
            Question.prompt,
            Question.typeform_ref,
            Question.order_number,
            SurveyVersion.revision
        )
        .join(SurveyVersion, SurveyVersion.survey_version_id == Question.survey_version_id)
        .filter(Question.survey_version_id.in_(version_ids))
        .order_by(SurveyVersion.revision.desc(), Question.order_number.asc())
        .all()
    )

    columns_od = OrderedDict()
    qid_to_colkey = {}

    for qid, prompt, tf_ref, _ord, rev in qrows:
        key = tf_ref or _norm_prompt(prompt)
        if key not in columns_od:
            columns_od[key] = {"id": key, "prompt": prompt, "revision": rev}
        qid_to_colkey[str(qid)] = key

    qcols = list(columns_od.values())

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
        .order_by(Response.submitted_at.desc(), Response.response_id)
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

        colkey = qid_to_colkey.get(str(r.question_id))
        if colkey:
            if entry["answers"].get(colkey, "-") == "-":
                entry["answers"][colkey] = val

    return jsonify({
        "questions": qcols,
        "responses": list(resp_map.values())
    })