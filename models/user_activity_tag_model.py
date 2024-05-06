from datetime import datetime, timezone

from db import db


class UserActivityTagModel(db.Model):
    __tablename__ = "user_activity_tag"

    user_activity_tag_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    activity_review_id = db.Column(db.Integer, db.ForeignKey('activity_review.activity_review_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # user = db.relationship("UserModel", back_populates="user_activity_tags")
    # activity_review = db.relationship("ActivityReviewModel", back_populates="user_activity_tags")

    def json(self):
        return {
            "user_activity_tag_id": self.user_activity_tag_id,
            "user_id": self.user_id,
            "activity_review_id": self.activity_review_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def find_by_id(cls, user_activity_tag_id):
        return cls.query.filter_by(user_activity_tag_id=user_activity_tag_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
