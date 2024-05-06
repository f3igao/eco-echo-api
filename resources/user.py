from flask import abort
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
    def post(self, user_data):
        user = UserModel(
            name=user_data["name"],
            email=user_data["email"],
            password=user_data["password"],
            created_at=user_data.get("created_at"),
            updated_at=user_data.get("updated_at")
        )
        user.save_to_db()
        return user


@blp.route("/<int:user_id>")
class UserItem(MethodView):
    @blp.response(status_code=200, schema=UserSchema)
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            abort(404, message="User not found")
        return user

    @blp.arguments(UpdateUserSchema)
    @blp.response(status_code=200, schema=UserSchema)
    def put(self, payload, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            abort(404, message="User not found")
        user.update_from_dict(payload)
        return user

    @blp.response(status_code=204)
    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            abort(404, message="User not found")
        user.delete_from_db()
        return
