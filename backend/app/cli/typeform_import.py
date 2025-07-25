import os, uuid, requests
from flask import current_app
from click import argument

from ..extensions import db
from ..models.survey import Survey, Question, Option, QuestionType
from ..models.option_set import OptionSet, QuestionOption

TYPEFORM_API = "https://api.typeform.com/forms/{form_id}"

def parse_float_from_label(label: str):
    try:
        return float(label.strip())
    except ValueError:
        if " - " in label:
            try:
                return float(label.split(" - ", 1)[0].strip())
            except ValueError:
                return None
        return None

def get_or_create(model, defaults=None, **filters):
    instance = model.query.filter_by(**filters).first()
    if instance:
        return instance, False
    params = dict(**filters)
    params.update(defaults or {})
    instance = model(**params)
    db.session.add(instance)
    return instance, True

def import_typeform_form(form_id: str):
    token = os.environ.get("TYPEFORM_TOKEN")
    if not token:
        raise RuntimeError("TYPEFORM_TOKEN not set in environment or not found")
    headers = {"Authorization": f"Bearer {token}"}

    r = requests.get(TYPEFORM_API.format(form_id=form_id), headers=headers)
    r.raise_for_status()
    form_json = r.json()

    survey, created = get_or_create(
        Survey,
        defaults={"description": form_json.get("title", "")},
        name=form_json.get("title", f"Typeform {form_id}")
    )

    if not created:
        raise ValueError("Survey already exists, aborting to prevent duplication")

    for field in form_json.get("fields", []):
        f_type = field.get("type")
        title = field.get("title", "").strip()

        if f_type == "multiple_choice":
            q = Question(
                survey_id=survey.survey_id,
                prompt=title,
                question_type=QuestionType.mcq
            )
            db.session.add(q)

            for choice in (field.get("properties", {}).get("choices") or []):
                label = choice.get("label", "")
                numeric = parse_float_from_label(label)
                opt = Option(
                    question=q,
                    label=label,
                    numeric_value=numeric
                )
                db.session.add(opt)

        elif f_type == "matrix":
            props = field.get("properties", {})
            columns = props.get("columns", [])
            rows = props.get("rows", [])

            if not columns or not rows:
                continue

            oset, _ = get_or_create(
                OptionSet,
                defaults={
                    "instructions": field.get("instructions", "")
                },
                name=f"Typeform:{form_id}:{field.get('id')}"
            )

            for col in columns:
                label = col.get("label", "")
                numeric = parse_float_from_label(label)
                opt, _ = get_or_create(
                    Option,
                    defaults={
                        "label": label,
                        "numeric_value": numeric,
                        "option_set_id": oset.option_set_id
                    },
                    option_set_id=oset.option_set_id,
                    label=label
                )

            for index, row in enumerate(rows, start=1):
                q = Question(
                    survey_id=survey.survey_id,
                    prompt=row.get("label", ""),
                    question_type=QuestionType.matrix,
                    option_set_id=oset.option_set_id,
                    order_number=index
                )
                db.session.add(q)

        elif f_type == "contact_info":
            q = Question(
                survey_id=survey.survey_id,
                prompt=title,
                question_type=QuestionType.contact
            )
            db.session.add(q)
        else:
            q = Question(
                survey_id=survey.survey_id,
                prompt=title,
                question_type=QuestionType.contact
            )
            db.session.add(q)

    db.session.commit()
    return survey.survey_id

from flask.cli import with_appcontext
import click

@click.command("typeform-import")
@argument("form_id")
@with_appcontext
def import_cmd(form_id):
    sid = import_typeform_form(form_id)
    click.echo(f"Imported Typeform {form_id} as Survey {sid}")