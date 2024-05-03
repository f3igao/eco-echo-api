from db import db
from datetime import datetime, timezone


class StateModel(db.Model):
    __tablename__ = "state"

    state_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    region = db.Column(db.String(255), nullable=False)
    abbreviation = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # parks = db.relationship("ParkModel", secondary="park_state", back_populates="states")

    def json(self):
        return {
            "state_id": self.state_id,
            "name": self.name,
            "region": self.region,
            "abbreviation": self.abbreviation,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def find_by_id(cls, state_id):
        return cls.query.filter_by(state_id=state_id).first()
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
