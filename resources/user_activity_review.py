import uuid
from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import fields, Schema

from models.user_activity_review_model import UserActivityReviewModel

blp = Blueprint("user_activity_review", "user_activity_review", url_prefix="/user_activity_reviews",
                description="User Activity Review API")


class CreateUserActivityReviewSchema(Schema):
    user_id = fields.Int(required=True)
    activity_review_id = fields.Int(required=True)
    rating = fields.Decimal(required=True)


class UpdateUserActivityReviewSchema(Schema):
    user_id = fields.Int()
    activity_review_id = fields.Int()
    rating = fields.Decimal()


class UserActivityReviewSchema(Schema):
    user_activity_review_id = fields.Int()
    user_id = fields.Int()
    activity_review_id = fields.Int()
    rating = fields.Decimal()


class UserActivityReviewListSchema(Schema):
    user_activity_reviews = fields.List(fields.Nested(UserActivityReviewSchema()))


@blp.route("")
class UserActivityReviewCollection(MethodView):
    @blp.response(status_code=200, schema=UserActivityReviewListSchema)
    def get(self):
        user_activity_reviews = UserActivityReviewModel.find_all()
        return {"user_activity_reviews": user_activity_reviews}

    @blp.arguments(CreateUserActivityReviewSchema)
    @blp.response(status_code=201, schema=UserActivityReviewSchema)
    def post(self, user_activity_review):
        new_user_activity_review = UserActivityReviewModel(**user_activity_review)
        new_user_activity_review.save_to_db()
        return new_user_activity_review.json(), 201


@blp.route("/<int:user_activity_review_id>")
class UserActivityReviewItem(MethodView):
    @blp.response(status_code=200, schema=UserActivityReviewSchema)
    def get(self, user_activity_review_id):
        user_activity_review = UserActivityReviewModel.find_by_id(user_activity_review_id)
        if not user_activity_review:
            abort(404, message=f"User Activity Review with ID {user_activity_review_id} not found")
        return user_activity_review.json()

    @blp.arguments(UpdateUserActivityReviewSchema)
    @blp.response(status_code=200, schema=UserActivityReviewSchema)
    def put(self, payload, user_activity_review_id):
        user_activity_review = UserActivityReviewModel.find_by_id(user_activity_review_id)
        if not user_activity_review:
            abort(404, message=f"User Activity Review with ID {user_activity_review_id} not found")
        user_activity_review.update(payload)
        return user_activity_review.json()

    @blp.response(status_code=204)
    def delete(self, user_activity_review_id):
        user_activity_review = UserActivityReviewModel.find_by_id(user_activity_review_id)
        if not user_activity_review:
            abort(404, message=f"User Activity Review with ID {user_activity_review_id} not found")
        user_activity_review.delete_from_db()
        return
