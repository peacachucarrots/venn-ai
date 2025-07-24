from ..extensions import db
import enum, uuid

class Survey(db.Model):
    __tablename__ = "surveys"

    survey_id    = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    name         = db.Column(db.String(), nullable=False)
    description  = db.Column(db.String())
    questions    = db.relationship(
        "Question",
        back_populates="survey",
        cascade="all, delete-orphan",
        order_by="Question.order_number"
    )
    responses    = db.relationship(
        "Response",
        back_populates="survey",
        cascade="all, delete-orphan"
    )

class QuestionType(enum.Enum):
    mcq      = "mcq"
    matrix   = "matrix"
    contact  = "contact"

class Question(db.Model):
    __tablename__  = "questions"

    question_id    = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    survey_id      = db.Column(db.UUID, db.ForeignKey("surveys.survey_id"), nullable=False)
    option_set_id  = db.Column(db.UUID, db.ForeignKey("option_sets.option_set_id"))
    prompt         = db.Column(db.String(), nullable=False)
    question_type  = db.Column(
        db.Enum(QuestionType, name="question_types"),
        nullable=False,
        default="mcq"
    )
    order_number   = db.Column(db.Integer, autoincrement=True)
    survey         = db.relationship("Survey", back_populates="questions")
    options        = db.relationship(
        "Option",
        back_populates="question",
        cascade="all, delete-orphan",
        order_by="Option.numeric_value"
    )
    answers        = db.relationship(
        "Answer",
        back_populates="question",
        cascade="all, delete-orphan"
    )
    shared_set     = db.relationship("OptionSet", back_populates="questions")
    via_set        = db.relationship(
        "Option",
        secondary="question_options",
        back_populates="questions"
    )

class Option(db.Model):
    __tablename__  = "options"

    option_id      = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    question_id    = db.Column(db.UUID, db.ForeignKey("questions.question_id"))
    option_set_id  = db.Column(db.UUID, db.ForeignKey("option_sets.option_set_id"))
    label          = db.Column(db.String())
    numeric_value  = db.Column(db.Numeric(scale=2))

    question       = db.relationship("Question", back_populates="options")
    answers        = db.relationship("Answer", back_populates="option")
    set            = db.relationship("OptionSet", back_populates="options")
    questions      = db.relationship(
        "Question",
        secondary="question_options",
        back_populates="via_set"
    )
