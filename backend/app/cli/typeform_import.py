from __future__ import annotations

import uuid, re, os, requests
from typing import Any, Dict

from ..extensions import db
from ..models.survey import Survey, Question, Option, QuestionType
from ..models.option_set import OptionSet

number_re = re.compile(r"^\s*(\d+(?:\.\d+)?)")
def _num_val(label: str) -> float | None:
    """Pull leading 1, 1.5, 2 … number from a choice label, else None."""
    m = number_re.match(label)
    return float(m.group(1)) if m else None


def import_typeform_form(form_id: str, commit: bool = True) -> uuid.UUID:
    """
    Accept a Typeform form-ID (str) and import it to DB.
    Return the newly generated survey_id.
    """
    # fetch JSON from Typeform
    res = requests.get(
        f"https://api.typeform.com/forms/{form_id}",
        headers={"Authorization": f"Bearer {os.environ['TYPEFORM_TOKEN']}"},
        timeout=20,
    )
    res.raise_for_status()
    form_json = res.json()

    # create the survey
    survey = Survey(
        name=form_json["title"].strip().title(),
        description=(form_json["welcome_screens"][0]["title"].strip()
                     if form_json.get("welcome_screens") else None),
    )
    db.session.add(survey)
    db.session.flush()

    question_order = 1

    # OptionSet for matrix questions
    def get_or_create_importance_set(field: Dict[str, Any]) -> OptionSet:
        name = "Importance Scale"
        imp_set = OptionSet.query.filter_by(name=name).first()
        if imp_set:
            return imp_set

        imp_set = OptionSet(
            name=name,
            instructions=field["title"].strip()
        )
        db.session.add(imp_set)

        for idx, ch in enumerate(field["properties"]["fields"][0]["properties"]["choices"]):
            db.session.add(Option(
                option_set_id=imp_set.option_set_id,
                label=ch["label"],
                numeric_value=idx + 1,       # 1‒4
            ))
        db.session.flush()
        return imp_set

    # ── 3.  Walk through each Typeform “field” ────────────────────────────
    for field in form_json["fields"]:

        ftype = field["type"]

        # MCQ
        if ftype == "multiple_choice":
            q = Question(
                survey_id=survey.survey_id,
                prompt=field["title"].strip(),
                question_type=QuestionType.mcq,
                order_number=question_order,
            )
            db.session.add(q)

            for idx, choice in enumerate(field["properties"]["choices"]):
                raw = choice["label"].strip()
                nv = _num_val(raw)
                if nv is None:
                    nv = idx + 1

                if _num_val(raw) is not None:
                    clean = re.sub(r"^\s*\d+(?:\.\d+)?\s*-\s*", "", raw).strip()
                else:
                    clean = raw
                opt = Option(
                    question_id=q.question_id,
                    label=clean,
                    numeric_value=nv,
                )
                q.options.append(opt)
                db.session.add(opt)

            question_order += 1

        # Matrix Question
        elif ftype == "matrix":
            imp_set = get_or_create_importance_set(field)

            for row in field["properties"]["fields"]:
                q = Question(
                    survey_id=survey.survey_id,
                    prompt=row["title"].strip(),
                    question_type=QuestionType.matrix,
                    option_set_id=imp_set.option_set_id,
                    order_number=question_order,
                )
                db.session.add(q)
                question_order += 1

        # contact question
        elif ftype == "contact_info":
            for sub in field["properties"]["fields"]:
                q = Question(
                    survey_id=survey.survey_id,
                    prompt=sub["title"].strip(),
                    question_type=QuestionType.contact,
                    order_number=question_order,
                )
                db.session.add(q)
                question_order += 1

    if commit:
        db.session.commit()

    return survey.survey_id

from flask.cli import with_appcontext
import click

@click.command("typeform-import")
@click.argument("form_id")
@click.option("--dry-run", is_flag=True, help="Don't commit, just log.")
@with_appcontext
def import_cmd(form_id, dry_run):
    sid = import_typeform_form(form_id, commit=not dry_run)
    click.echo(f"Would have imported as Survey {sid}" if dry_run else f"Imported -> {sid}")