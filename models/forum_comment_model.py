from datetime import datetime, timezone

from db import db


class ForumCommentModel(db.Model):
    __tablename__ = "forum_comment"

    comment_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_post.post_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    post = db.relationship("ForumPostModel", back_populates="comments")
    user = db.relationship("UserModel", back_populates="forum_comments")

    @property
    def user_name(self):
        return self.user.name if self.user else None

    @classmethod
    def find_by_id(cls, comment_id):
        return db.session.get(cls, comment_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
