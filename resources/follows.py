from flask import abort, request
from flask.views import MethodView
from flask_smorest import Blueprint

from models.follow_model import FollowModel
from models.user_model import UserModel
from schemas.follow_schema import (
    CreateFollowSchema,
    FollowSchema,
    FollowStatusSchema,
    FollowUserListSchema,
)

blp = Blueprint("follows", "follows", url_prefix="/api/follows", description="Follow API")


@blp.route("")
class FollowCollection(MethodView):
    @blp.arguments(CreateFollowSchema)
    @blp.response(status_code=201, schema=FollowSchema)
    def post(self, data):
        follower_id = data["follower_id"]
        following_id = data["following_id"]

        if follower_id == following_id:
            abort(400, message="You cannot follow yourself")
        if not UserModel.find_by_id(follower_id):
            abort(404, message="Follower user not found")
        if not UserModel.find_by_id(following_id):
            abort(404, message="User to follow not found")

        existing = FollowModel.find_by_ids(follower_id, following_id)
        if existing:
            abort(409, message="Already following this user")

        follow = FollowModel(follower_id=follower_id, following_id=following_id)
        follow.save_to_db()
        return follow

    @blp.arguments(CreateFollowSchema)
    @blp.response(status_code=204)
    def delete(self, data):
        follower_id = data["follower_id"]
        following_id = data["following_id"]

        follow = FollowModel.find_by_ids(follower_id, following_id)
        if not follow:
            abort(404, message="Follow relationship not found")
        follow.delete_from_db()
        return


@blp.route("/followers/<int:user_id>")
class FollowerList(MethodView):
    @blp.response(status_code=200, schema=FollowUserListSchema)
    def get(self, user_id):
        follows = FollowModel.find_followers(user_id)
        users = [f.follower_user for f in follows]
        return {"users": users, "total": len(users)}


@blp.route("/following/<int:user_id>")
class FollowingList(MethodView):
    @blp.response(status_code=200, schema=FollowUserListSchema)
    def get(self, user_id):
        follows = FollowModel.find_following(user_id)
        users = [f.followed_user for f in follows]
        return {"users": users, "total": len(users)}


@blp.route("/status")
class FollowStatus(MethodView):
    @blp.response(status_code=200, schema=FollowStatusSchema)
    def get(self):
        follower_id = request.args.get("follower_id", type=int)
        following_id = request.args.get("following_id", type=int)
        if not follower_id or not following_id:
            abort(400, message="follower_id and following_id query params are required")
        follow = FollowModel.find_by_ids(follower_id, following_id)
        return {"is_following": follow is not None}
