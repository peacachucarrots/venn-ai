from sqlalchemy.orm import selectinload

from ....extensions import db
from ....models.survey import Option
from ....models.option_set import OptionSet

def get_or_create_option_set_from_choices(name: str, instructions: str, choices: list[dict[str, str]]) -> OptionSet:
    """
    Given a choice list from Typeform, return an OptionSet that exactly matches
    those choices (label + numeric_value).  Reuse an existing set if the label
    sequence already exists; otherwise create a fresh one.

    No rows are ever deleted, so existing Answer FKs stay valid.
    """
    desired_labels = [c["label"] for c in choices]

    # pull every OptionSet with given name
    candidates = (
        OptionSet.query
        .filter_by(name=name)
        .options(selectinload(OptionSet.options))
        .all()
    )

    # check if OptionSet already matches one in DB
    for os in candidates:
        labels = [o.label.strip() for o in sorted(os.options, key=lambda o: o.numeric_value)]
        if labels == desired_labels:
            return os

    # no match, create new OptionSet
    opt_set = OptionSet(name=name, instructions=instructions)
    db.session.add(opt_set)
    db.session.flush()

    for idx, choice in enumerate(choices):
        db.session.add(
            Option(
                option_set_id=opt_set.option_set_id,
                label=choice["label"],
                numeric_value=idx + 1,
            )
        )
    db.session.flush()
    return opt_set
