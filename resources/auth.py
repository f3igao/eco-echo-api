from datetime import datetime, timezone

from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from werkzeug.security import generate_password_hash

from models.user_model import UserModel
from schemas.user_schema import CreateUserSchema, UserSchema

blp = Blueprint("auth", "auth", url_prefix="/api/auth", description="Authentication API")


@blp.route("/register")
class Register(MethodView):
    @blp.arguments(CreateUserSchema)
    @blp.response(status_code=201, schema=UserSchema)
    def post(self, user_data):
        if UserModel.find_by_email(user_data["email"]):
            abort(409, message="A user with that email already exists.")

        now = datetime.now(timezone.utc)
        user = UserModel(
            name=user_data["name"],
            email=user_data["email"],
            password=generate_password_hash(user_data["password"], method="pbkdf2:sha256"),
            created_at=now,
            updated_at=now,
        )
        user.save_to_db()
        return user
