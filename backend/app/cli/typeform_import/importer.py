from __future__ import annotations

import uuid, click

from ...extensions import db
from ...models.survey import Survey, SurveyVersion
from .helpers.typeform_utils import _hash_schema, fetch_json
from .helpers.question_adder import add_multiple_choice, add_matrix, add_contact


def import_typeform_form(form_id: str, commit: bool = True, force: bool = False) -> uuid.UUID:
    """
    Import or re‑import a Typeform survey.
    Returns the survey_id (not the version id) that was affected.
    """
    form = fetch_json(form_id)
    schema_hash = _hash_schema(form)

    # check if survey already exists in DB
    survey = Survey.query.filter_by(typeform_id=form_id).first()
    if not survey:
        survey = Survey(
            typeform_id=form_id,
            name=form["title"].title(),
            description=(
                form["welcome_screens"][0]["title"]
                if form.get("welcome_screens") else None
            ),
        )
        db.session.add(survey)
        db.session.flush()

    # compare against latest active version of survey for changes
    latest = (
        SurveyVersion.query
        .filter_by(survey_id=survey.survey_id, is_active=True)
        .order_by(SurveyVersion.revision.desc())
        .first()
    )

    if not force and latest and latest.schema_hash == schema_hash:
        click.echo("Schema already in DB; no changes detected.")
        return survey.survey_id

    # changes detected, create new revision
    new_revision = (latest.revision + 1) if latest else 1
    if latest:
        latest.is_active = False

    version = SurveyVersion(
        survey_id=survey.survey_id,
        revision=new_revision,
        is_active=True,
        schema_hash=schema_hash,
    )
    db.session.add(version)
    db.session.flush()

    # walk through typeform fields
    question_order = 1
    for field in form["fields"]:
        ftype = field["type"]

        if ftype == "multiple_choice":
            question_order += add_multiple_choice(field, version.survey_version_id, question_order)

        elif ftype == "matrix":
            question_order += add_matrix(field, version.survey_version_id, question_order)

        elif ftype == "contact_info":
            question_order += add_contact(field, version.survey_version_id, question_order)

    if commit:
        click.echo(f"Imported revision {new_revision} for Survey {survey.survey_id} ({survey.name})")
        db.session.commit()

    return survey.survey_id
