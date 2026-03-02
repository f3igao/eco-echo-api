from datetime import datetime, timezone

from db import db


class ForumPostModel(db.Model):
    __tablename__ = "forum_post"

    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    park_id = db.Column(db.Integer, db.ForeignKey('park.park_id'), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user = db.relationship("UserModel", back_populates="forum_posts")
    park = db.relationship("ParkModel", back_populates="forum_posts")
    comments = db.relationship("ForumCommentModel", back_populates="post", cascade="all, delete-orphan")

    @property
    def comment_count(self):
        return len(self.comments)

    @property
    def user_name(self):
        return self.user.name if self.user else None

    @property
    def park_name(self):
        return self.park.name if self.park else None

    @classmethod
    def find_by_id(cls, post_id):
        return db.session.get(cls, post_id)

    @classmethod
    def find_all(cls, park_id=None, search=None, limit=20, offset=0):
        query = cls.query
        if park_id:
            query = query.filter_by(park_id=park_id)
        if search:
            query = query.filter(
                db.or_(cls.title.ilike(f'%{search}%'), cls.body.ilike(f'%{search}%'))
            )
        return query.order_by(cls.created_at.desc()).limit(limit).offset(offset).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
