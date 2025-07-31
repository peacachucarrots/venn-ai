from ..extensions import db
import uuid

class OptionSet(db.Model):
    __tablename__ = "option_sets"

    option_set_id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)

    name = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String)

    options = db.relationship(
        "Option",
        back_populates="set",
        order_by="Option.numeric_value"
    )
    questions = db.relationship(
        "Question",
        back_populates="option_set",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

class QuestionOption(db.Model):
    __tablename__ = "question_options"

    question_id = db.Column(
        db.UUID,
        db.ForeignKey("questions.question_id"),
        primary_key=True
    )
    option_id = db.Column(
        db.UUID,
        db.ForeignKey("options.option_id"),
        primary_key=True
    )
