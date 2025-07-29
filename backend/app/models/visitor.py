from ..extensions import db
import uuid

class Visitor(db.Model):
    __tablename__ = "visitors"

    visitor_id    = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)

    first_name    = db.Column(db.String)
    last_name     = db.Column(db.String)
    email         = db.Column(db.String, index=True)
    phone         = db.Column(db.String)
    company       = db.Column(db.String)

    responses     = db.relationship(
        "Response",
        back_populates="visitor",
        cascade="all, delete-orphan"
    )