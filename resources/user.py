import uuid

from flask.views import MethodView
from flask_smorest import Blueprint

from models.user_model import UserModel
from schemas.user_schema import CreateUserSchema, UserSchema, UserListSchema, UpdateUserSchema

blp = Blueprint("user", "user", url_prefix="/users", description="User API")


@blp.route("")
class UserCollection(MethodView):
    @blp.response(status_code=200, schema=UserListSchema)
    def get(self):
        users = UserModel.query.all()
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
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()

    @blp.arguments(UpdateUserSchema)
    @blp.response(status_code=200, schema=UserSchema)
    def put(self, payload, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        # Your logic to update a user by ID
        return user.json()

    @blp.response(status_code=204)
    def delete(self, user_id):
        pass
