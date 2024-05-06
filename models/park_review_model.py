from datetime import datetime, timezone

from db import db


class ParkReviewModel(db.Model):
    __tablename__ = "park_review"

    park_review_id = db.Column(db.Integer, primary_key=True)
    park_id = db.Column(db.Integer, db.ForeignKey('park.park_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    visit_date = db.Column(db.Date, nullable=False)
    comment = db.Column(db.Text)
    media_url = db.Column(db.String(255))
    is_private = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user = db.relationship("UserModel", back_populates="park_reviews")
    park = db.relationship("ParkModel", back_populates="park_reviews")

    def json(self):
        return {
            "park_review_id": self.park_review_id,
            "park_id": self.park_id,
            "user_id": self.user_id,
            "rating": self.rating,
            "visit_date": self.visit_date,
            "comment": self.comment,
            "media_url": self.media_url,
            "is_private": self.is_private,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def find_by_id(cls, park_review_id):
        return cls.query.filter_by(park_review_id=park_review_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
