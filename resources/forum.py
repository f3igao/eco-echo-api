from flask import abort, request
from flask.views import MethodView
from flask_smorest import Blueprint

from models.forum_comment_model import ForumCommentModel
from models.forum_post_model import ForumPostModel
from models.user_model import UserModel
from schemas.forum_schema import (
    CreateForumCommentSchema,
    CreateForumPostSchema,
    ForumCommentSchema,
    ForumPostDetailSchema,
    ForumPostListSchema,
    ForumPostSchema,
)

blp = Blueprint("forum", "forum", url_prefix="/api/forum", description="Forum API")


@blp.route("/posts")
class ForumPostCollection(MethodView):
    @blp.response(status_code=200, schema=ForumPostListSchema)
    def get(self):
        park_id = request.args.get("park_id", type=int)
        search = request.args.get("search", type=str)
        limit = request.args.get("limit", default=20, type=int)
        offset = request.args.get("offset", default=0, type=int)
        posts = ForumPostModel.find_all(park_id=park_id, search=search, limit=limit, offset=offset)
        return {"posts": posts, "total": len(posts)}

    @blp.arguments(CreateForumPostSchema)
    @blp.response(status_code=201, schema=ForumPostSchema)
    def post(self, data):
        if not UserModel.find_by_id(data["user_id"]):
            abort(404, message="User not found")
        post = ForumPostModel(
            user_id=data["user_id"],
            title=data["title"],
            body=data["body"],
            park_id=data.get("park_id"),
        )
        post.save_to_db()
        return post


@blp.route("/posts/<int:post_id>")
class ForumPostItem(MethodView):
    @blp.response(status_code=200, schema=ForumPostDetailSchema)
    def get(self, post_id):
        post = ForumPostModel.find_by_id(post_id)
        if not post:
            abort(404, message="Post not found")
        return post

    @blp.response(status_code=204)
    def delete(self, post_id):
        user_id = request.args.get("user_id", type=int)
        post = ForumPostModel.find_by_id(post_id)
        if not post:
            abort(404, message="Post not found")
        if user_id and post.user_id != user_id:
            abort(403, message="You can only delete your own posts")
        post.delete_from_db()
        return


@blp.route("/posts/<int:post_id>/comments")
class ForumCommentCollection(MethodView):
    @blp.arguments(CreateForumCommentSchema)
    @blp.response(status_code=201, schema=ForumCommentSchema)
    def post(self, data, post_id):
        post = ForumPostModel.find_by_id(post_id)
        if not post:
            abort(404, message="Post not found")
        if not UserModel.find_by_id(data["user_id"]):
            abort(404, message="User not found")
        comment = ForumCommentModel(
            post_id=post_id,
            user_id=data["user_id"],
            body=data["body"],
        )
        comment.save_to_db()
        return comment


@blp.route("/comments/<int:comment_id>")
class ForumCommentItem(MethodView):
    @blp.response(status_code=204)
    def delete(self, comment_id):
        user_id = request.args.get("user_id", type=int)
        comment = ForumCommentModel.find_by_id(comment_id)
        if not comment:
            abort(404, message="Comment not found")
        if user_id and comment.user_id != user_id:
            abort(403, message="You can only delete your own comments")
        comment.delete_from_db()
        return
