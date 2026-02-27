from datetime import datetime, timezone

from db import db


class WishlistModel(db.Model):
    __tablename__ = "wishlist"

    wishlist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    park_id = db.Column(db.Integer, db.ForeignKey('park.park_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    user = db.relationship("UserModel", back_populates="wishlists")
    park = db.relationship("ParkModel", back_populates="wishlists")

    def json(self):
        return {
            "wishlist_id": self.wishlist_id,
            "user_id": self.user_id,
            "park_id": self.park_id,
            "created_at": self.created_at,
        }

    @classmethod
    def find_by_id(cls, wishlist_id):
        return db.session.get(cls, wishlist_id)

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()

    @classmethod
    def find_by_user_and_park(cls, user_id, park_id):
        return cls.query.filter_by(user_id=user_id, park_id=park_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
