import uuid
from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import fields, Schema

from models.user_activity_tag_model import UserActivityTagModel

blp = Blueprint("user_activity_tag", "user_activity_tag", url_prefix="/user_activity_tags",
                description="User Activity Tag API")


class CreateUserActivityTagSchema(Schema):
    user_id = fields.Int(required=True)
    activity_review_id = fields.Int(required=True)


class UserActivityTagSchema(Schema):
    user_activity_tag_id = fields.Int()
    user_id = fields.Int()
    activity_review_id = fields.Int()


class UserActivityTagListSchema(Schema):
    user_activity_tags = fields.List(fields.Nested(UserActivityTagSchema()))


@blp.route("")
class UserActivityTagCollection(MethodView):
    @blp.response(status_code=200, schema=UserActivityTagListSchema)
    def get(self):
        user_activity_tags = UserActivityTagModel.find_all()
        return {"user_activity_tags": user_activity_tags}

    @blp.arguments(CreateUserActivityTagSchema)
    @blp.response(status_code=201, schema=UserActivityTagSchema)
    def post(self, user_activity_tag):
        new_user_activity_tag = UserActivityTagModel(**user_activity_tag)
        new_user_activity_tag.save_to_db()
        return new_user_activity_tag.json(), 201


@blp.route("/<int:user_activity_tag_id>")
class UserActivityTagItem(MethodView):
    @blp.response(status_code=200, schema=UserActivityTagSchema)
    def get(self, user_activity_tag_id):
        user_activity_tag = UserActivityTagModel.find_by_id(user_activity_tag_id)
        if not user_activity_tag:
            abort(404, message=f"User Activity Tag with ID {user_activity_tag_id} not found")
        return user_activity_tag.json()

    @blp.response(status_code=204)
    def delete(self, user_activity_tag_id):
        user_activity_tag = UserActivityTagModel.find_by_id(user_activity_tag_id)
        if not user_activity_tag:
            abort(404, message=f"User Activity Tag with ID {user_activity_tag_id} not found")
        user_activity_tag.delete_from_db()
        return
