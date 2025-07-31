from ..extensions import db
import uuid

class Response(db.Model):
    __tablename__ = "responses"

    response_id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    survey_version_id = db.Column(
        db.UUID,
        db.ForeignKey("survey_versions.survey_version_id", ondelete="CASCADE"),
        nullable=False
    )
    visitor_id = db.Column(
        db.UUID,
        db.ForeignKey("visitors.visitor_id"),
        nullable=False
    )

    analysis = db.Column(db.String())
    submitted_at = db.Column(db.DateTime)

    version = db.relationship("SurveyVersion", back_populates="responses")
    visitor = db.relationship("Visitor", back_populates="responses")
    answers = db.relationship(
        "Answer",
        back_populates="response",
        cascade="all, delete-orphan"
    )

class Answer(db.Model):
    __tablename__ = "answers"

    answer_id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    question_id = db.Column(db.UUID, db.ForeignKey("questions.question_id"), nullable=False)
    option_id = db.Column(db.UUID, db.ForeignKey("options.option_id"))
    response_id = db.Column(db.UUID, db.ForeignKey("responses.response_id"), nullable=False)

    free_text = db.Column(db.String())
    numeric_value = db.Column(db.Numeric(scale=2))

    question = db.relationship("Question", back_populates="answers")
    option = db.relationship("Option", back_populates="answers")
    response = db.relationship("Response", back_populates="answers")
