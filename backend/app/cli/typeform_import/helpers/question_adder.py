import re

from .option_sets import get_or_create_option_set_from_choices
from .typeform_utils import _num_val
from ....extensions import db
from ....models.survey import Question, QuestionType, Option

def add_multiple_choice(field, version_id, order_no) -> int:
    """Create one MC Question and its options. Return rows added (1)."""
    q = Question(
        survey_version_id=version_id,
        prompt=field["title"],
        question_type=QuestionType.mcq,
        order_number=order_no
    )
    db.session.add(q)
    db.session.flush()

    for idx, choice in enumerate(field["properties"]["choices"]):
        raw = choice["label"]
        num_val = _num_val(raw) or (idx + 1)
        clean = re.sub(r"^\s*\d+(?:\.\d+)?\s*-\s*", "", raw).strip() if _num_val(raw) else raw

        q.options.append(Option(label=clean, numeric_value=num_val))
    return 1

def add_matrix(field, version_id, order_no) -> int:
    """Create N matrix row questions. Return N."""
    choices = field["properties"]["fields"][0]["properties"]["choices"]
    imp_set = get_or_create_option_set_from_choices(
        name="Importance Scale",
        instructions=field["title"],
        choices=choices
    )

    rows_added = 0
    for row in field["properties"]["fields"]:
        db.session.add(
            Question(
                survey_version_id=version_id,
                prompt=row["title"],
                question_type=QuestionType.matrix,
                option_set_id=imp_set.option_set_id,
                order_number=order_no + rows_added
            )
        )
        rows_added += 1
    return rows_added

def add_contact(field, version_id, order_no) -> int:
    """Create N contact sub-questions. Return N."""
    rows_added = 0
    for sub in field["properties"]["fields"]:
        db.session.add(
            Question(
                survey_version_id=version_id,
                prompt=sub["title"],
                question_type=QuestionType.contact,
                order_number=order_no + rows_added
            )
        )
        rows_added += 1
    return rows_added
