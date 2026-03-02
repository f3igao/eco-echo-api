from datetime import datetime, timezone

from db import db


class UserModel(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_private = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    park_reviews = db.relationship("ParkReviewModel", back_populates="user")
    parks = db.relationship("ParkModel", secondary="park_review", back_populates="users")
    wishlists = db.relationship("WishlistModel", back_populates="user")
    followers = db.relationship("FollowModel", foreign_keys="[FollowModel.following_id]", back_populates="followed_user")
    following = db.relationship("FollowModel", foreign_keys="[FollowModel.follower_id]", back_populates="follower_user")
    forum_posts = db.relationship("ForumPostModel", back_populates="user")
    forum_comments = db.relationship("ForumCommentModel", back_populates="user")

    @property
    def follower_count(self):
        return len(self.followers)

    @property
    def following_count(self):
        return len(self.following)

    def json(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "is_private": self.is_private,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def update_from_dict(self, data):
        allowed = {"name", "email", "password", "is_private"}
        for key, value in data.items():
            if key in allowed and value is not None:
                setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()

    @classmethod
    def find_by_id(cls, user_id):
        return db.session.get(cls, user_id)

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
