from datetime import datetime, timezone

from db import db


class ActivityModel(db.Model):
    __tablename__ = "activity"

    activity_id = db.Column(db.Integer, primary_key=True)
    park_id = db.Column(db.Integer, db.ForeignKey('park.park_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.Float(precision=2), nullable=False)
    require_special_equipment = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    users = db.relationship("UserModel", secondary="activity_review", back_populates="activities")
    park = db.relationship("ParkModel", back_populates="activities")
    activity_reviews = db.relationship("ActivityReviewModel", back_populates="activity")

    def json(self):
        return {
            "activity_id": self.activity_id,
            "park_id": self.park_id,
            "name": self.name,
            "description": self.description,
            "duration": self.duration,
            "difficulty": self.difficulty,
            "require_special_equipment": self.require_special_equipment,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def find_by_id(cls, activity_id):
        return cls.query.filter_by(activity_id=activity_id).first()

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
