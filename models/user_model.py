from db import db
from models.activity_model import ActivityModel
from models.activity_review_model import ActivityReviewModel
from models.park_review_model import ParkReviewModel


class UserModel(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    parks = db.relationship("ParkModel", secondary="park_review", back_populates="users")
    park_reviews = db.relationship("ParkReviewModel", back_populates="user")
    activities = db.relationship("ActivityModel", secondary="activity_review", back_populates="users")
    activity_reviews = db.relationship("ActivityReviewModel", back_populates="user")

    def json(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
