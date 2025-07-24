from ..extensions import db
import uuid

class Visitor(db.Model):
    __tablename__ = "visitors"

    visitor_id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)

    responses = db.relationship(
        "Response",
        back_populates="visitor",
        cascade="all, delete-orphan"
    )