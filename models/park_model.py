from datetime import datetime, timezone

from db import db


class ParkModel(db.Model):
    __tablename__ = "park"

    park_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    established_date = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    visitor_count = db.Column(db.Integer, nullable=False)
    website = db.Column(db.String(255), nullable=False)
    entrance_info = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    activities = db.relationship("ActivityModel", back_populates="park")
    park_reviews = db.relationship("ParkReviewModel", back_populates="park")
    users = db.relationship("UserModel", secondary="park_review", back_populates="parks")
    states = db.relationship("StateModel", secondary="park_state", back_populates="parks")

    def json(self):
        return {
            "park_id": self.park_id,
            "name": self.name,
            "location": self.location,
            "description": self.description,
            "established_date": self.established_date,
            "size": self.size,
            "visitor_count": self.visitor_count,
            "website": self.website,
            "entrance_info": self.entrance_info,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def find_by_id(cls, park_id):
        return cls.query.filter_by(park_id=park_id).first()

    @classmethod
    def find_by_name(cls, name):
        db.session.commit()
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
