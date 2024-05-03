from datetime import datetime, timezone

from db import db


class UserActivityReviewModel(db.Model):
    __tablename__ = "user_activity_review"

    user_activity_review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    activity_review_id = db.Column(db.Integer, db.ForeignKey('activity_review.activity_review_id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # user = db.relationship("UserModel", back_populates="user_activity_reviews")

    def json(self):
        return {
            "user_activity_review_id": self.user_activity_review_id,
            "user_id": self.user_id,
            "activity_review_id": self.activity_review_id,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def find_by_id(cls, user_activity_review_id):
        return cls.query.filter_by(user_activity_review_id=user_activity_review_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
