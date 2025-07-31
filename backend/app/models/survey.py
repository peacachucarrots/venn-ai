from ..extensions import db
import enum, uuid
from datetime import datetime as dt

class Survey(db.Model):
    __tablename__ = "surveys"

    survey_id    = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    typeform_id  = db.Column(db.String(16), unique=True, index=True)

    name         = db.Column(db.String(), nullable=False)
    description  = db.Column(db.String())

    versions     = db.relationship(
        "SurveyVersion",
        back_populates="survey",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="SurveyVersion.revision.desc()"
    )

    @property
    def questions(self):
        """Return questions for the active version (read‑only)."""
        return self.active_version.questions if self.active_version else []

    @property
    def active_version(self):
        return next((v for v in self.versions if v.is_active), None)

class SurveyVersion(db.Model):
    __tablename__     = "survey_versions"

    survey_version_id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    survey_id         = db.Column(db.UUID, db.ForeignKey('surveys.survey_id', ondelete="CASCADE"), nullable=False)
    revision          = db.Column(db.Integer, nullable=False)
    imported_at       = db.Column(db.DateTime, default=dt.utcnow, nullable=False)
    is_active         = db.Column(db.Boolean, default=True, nullable=False)
    schema_hash       = db.Column(db.String(64))

    survey            = db.relationship("Survey", back_populates="versions")
    questions         = db.relationship(
        "Question",
        back_populates="version",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    responses = db.relationship(
        "Response",
        back_populates="version",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    __table_args__    = (
        db.UniqueConstraint("survey_id", "revision"),
        db.Index("uq_active_version_per_survey", "survey_id",
                 unique=True, postgresql_where=db.text("is_active")),
    )

class QuestionType(enum.Enum):
    mcq       = "mcq"
    matrix    = "matrix"
    contact   = "contact"

class Question(db.Model):
    __tablename__     = "questions"

    question_id       = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    survey_version_id = db.Column(db.UUID,
                                  db.ForeignKey("survey_versions.survey_version_id",
                                                ondelete="CASCADE"),
                                  nullable=False)
    option_set_id     = db.Column(db.UUID, db.ForeignKey("option_sets.option_set_id"))
    prompt            = db.Column(db.String(), nullable=False)
    question_type     = db.Column(
        db.Enum(QuestionType, name="question_types"),
        nullable=False,
        default="mcq"
    )
    order_number      = db.Column(db.Integer, autoincrement=True)
    options           = db.relationship(
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
    option_set     = db.relationship("OptionSet", back_populates="questions", foreign_keys=[option_set_id])
    via_set        = db.relationship(
        "Option",
        secondary="question_options",
        back_populates="questions"
    )
    version = db.relationship("SurveyVersion", back_populates="questions")

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
