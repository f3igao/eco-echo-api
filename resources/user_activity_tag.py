import uuid
from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import fields, Schema

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
        # Your logic to fetch user activity tags
        user_activity_tags = []
        return {"user_activity_tags": user_activity_tags}

    @blp.arguments(CreateUserActivityTagSchema)
    @blp.response(status_code=201, schema=UserActivityTagSchema)
    def post(self, user_activity_tag):
        user_activity_tag_id = uuid.uuid4().int  # Generate a unique ID for the user activity tag
        user_activity_tag["user_activity_tag_id"] = user_activity_tag_id
        # Your logic to create a new user activity tag
        return user_activity_tag

@blp.route("/<int:user_activity_tag_id>")
class UserActivityTagItem(MethodView):
    @blp.response(status_code=200, schema=UserActivityTagSchema)
    def get(self, user_activity_tag_id):
        # Your logic to fetch a user activity tag by ID
        user_activity_tag = {}
        return user_activity_tag

    @blp.response(status_code=204)
    def delete(self, user_activity_tag_id):
        # Your logic to delete a user activity tag by ID
        pass
