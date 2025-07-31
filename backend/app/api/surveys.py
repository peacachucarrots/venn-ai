from flask import Blueprint, jsonify, abort
from ..models.survey import Survey, QuestionType

bp = Blueprint("surveys", __name__, url_prefix="/api/surveys")

WELCOME_SURVEY_NAME = "Quantum Diagnostic"

@bp.get("/welcome")
def get_welcome_survey():
    """Returns the welcome survey survey_id"""
    welcome_survey = Survey.query.filter_by(name=WELCOME_SURVEY_NAME).first()
    if not welcome_survey:
        abort(404, "No welcome survey found")

    return jsonify(welcome_survey.survey_id)

@bp.get("/")
def get_surveys():
    """Returns a list of all surveys"""
    surveys = Survey.query.order_by(Survey.name).all()
    return jsonify(
        [
            {
                "survey_id": str(s.survey_id),
                "name": s.name,
                "description": s.description or "",
            }
            for s in surveys
        ]
    )

@bp.get("/<uuid:survey_id>")
def get_survey(survey_id):
    """Returns a survey by survey_id"""
    # determine survey and survey version
    survey = Survey.query.get_or_404(survey_id)
    version = survey.active_version
    if not version:
        abort(404, "Survey has no active version")

    # build question payload for survey
    questions_payload = []
    for q in version.questions:
        if q.question_type == QuestionType.matrix and q.option_set_id:
            opts = q.option_set.options
            shared_block = {
                "option_set_id": str(q.option_set.option_set_id),
                "name": q.option_set.name,
                "instructions": q.option_set.instructions,
                "options": [
                    {
                        "option_id": str(o.option_id),
                        "label": o.label or "",
                        "numeric_value": float(o.numeric_value),
                    }
                    for o in opts
                ],
            }
        else:
            opts = q.options
            shared_block = None

        questions_payload.append(
            {
                "question_id": str(q.question_id),
                "prompt": q.prompt,
                "question_type": q.question_type.value
                if hasattr(q.question_type, "value")
                else q.question_type,
                "option_set_id": str(q.option_set_id) if q.option_set_id else None,
                "shared_set": shared_block,
                "options": [
                    {
                        "option_id": str(o.option_id),
                        "label": o.label or "",
                        "numeric_value": float(o.numeric_value),
                    }
                    for o in opts
                ],
            }
        )

    return jsonify(
        {
            "survey_id": str(survey.survey_id),
            "survey_version_id": str(version.survey_version_id),
            "name": survey.name,
            "description": survey.description or "",
            "questions": questions_payload,
        }
    )
