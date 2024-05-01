import uuid
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import fields, Schema

blp = Blueprint("user", "user", url_prefix="/users", description="User API")


class CreateUserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    timestamp = fields.DateTime(required=True)
    last_modified = fields.DateTime(required=True)


class UpdateUserSchema(Schema):
    email = fields.Email()
    password = fields.Str()
    timestamp = fields.DateTime()
    last_modified = fields.DateTime()


class UserSchema(Schema):
    user_id = fields.Int()
    email = fields.Email()
    password = fields.Str()
    timestamp = fields.DateTime()
    last_modified = fields.DateTime()


class UserListSchema(Schema):
    users = fields.List(fields.Nested(UserSchema()))


@blp.route("")
class UserCollection(MethodView):
    @blp.response(status_code=200, schema=UserListSchema)
    def get(self):
        # Your logic to fetch users
        users = []
        return {"users": users}

    @blp.arguments(CreateUserSchema)
    @blp.response(status_code=201, schema=UserSchema)
    def post(self, user):
        user_id = uuid.uuid4().int  # Generate a unique ID for the user
        user["user_id"] = user_id
        # Your logic to create a new user
        return user


@blp.route("/<int:user_id>")
class UserItem(MethodView):
    @blp.response(status_code=200, schema=UserSchema)
    def get(self, user_id):
        # Your logic to fetch a user by ID
        user = {}
        return user

    @blp.arguments(UpdateUserSchema)
    @blp.response(status_code=200, schema=UserSchema)
    def put(self, payload, user_id):
        # Your logic to update a user by ID
        user = {}
        return user

    @blp.response(status_code=204)
    def delete(self, user_id):
        pass

