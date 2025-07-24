from flask import Blueprint, jsonify
from ..models.survey import Survey, QuestionType

bp = Blueprint('surveys', __name__, url_prefix='/api/surveys')

@bp.get("/")
def get_surveys():
    surveys = Survey.query.order_by(Survey.name).all()
    return jsonify ([
        {
            "survey_id": str(s.survey_id),
            "name": s.name,
            "description": s.description or ""
        }
        for s in surveys
    ])

@bp.get("/<uuid:survey_id>")
def get_survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)

    from ..models.option_set import OptionSet
    importance_set = OptionSet.query.filter_by(name="Importance Scale").first()
    shared_opts = importance_set.options if importance_set else []

    questions_payload = []
    for q in survey.questions:
        if q.question_type is QuestionType.matrix and q.shared_set:
            opts = q.shared_set.options
        else:
            opts = q.options

        questions_payload.append({
            "question_id": str(q.question_id),
            "prompt": q.prompt,
            "question_type": q.question_type.value if hasattr(q.question_type, "value") else q.question_type,
            "option_set_id": str(q.option_set_id) if q.option_set_id else None,
            "shared_set": q.shared_set and {
                "option_set_id": str(q.shared_set.option_set_id),
                "name": q.shared_set.name,
                "instructions": q.shared_set.instructions,
                "options": [
                    {
                        "option_id": str(o.option_id),
                        "label": o.label or "",
                        "numeric_value": float(o.numeric_value)
                    } for o in opts
                ]
            },
            "options": [
                {
                    "option_id": str(o.option_id),
                    "label": o.label or "",
                    "numeric_value": float(o.numeric_value)
                } for o in opts
            ]
        })

    return jsonify({
        "survey_id": str(survey.survey_id),
        "name": survey.name,
        "description": survey.description or "",
        "questions": questions_payload
    })