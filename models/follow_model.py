from datetime import datetime, timezone

from db import db


class FollowModel(db.Model):
    __tablename__ = "follow"

    follow_id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    following_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    __table_args__ = (
        db.UniqueConstraint('follower_id', 'following_id', name='uq_follow'),
    )

    follower_user = db.relationship("UserModel", foreign_keys=[follower_id], back_populates="following")
    followed_user = db.relationship("UserModel", foreign_keys=[following_id], back_populates="followers")

    @classmethod
    def find_by_ids(cls, follower_id, following_id):
        return cls.query.filter_by(follower_id=follower_id, following_id=following_id).first()

    @classmethod
    def find_followers(cls, user_id):
        return cls.query.filter_by(following_id=user_id).all()

    @classmethod
    def find_following(cls, user_id):
        return cls.query.filter_by(follower_id=user_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
