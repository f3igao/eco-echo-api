import uuid
from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import fields, Schema

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
        # Your logic to fetch user activity reviews
        user_activity_reviews = []
        return {"user_activity_reviews": user_activity_reviews}

    @blp.arguments(CreateUserActivityReviewSchema)
    @blp.response(status_code=201, schema=UserActivityReviewSchema)
    def post(self, user_activity_review):
        user_activity_review_id = uuid.uuid4().int  # Generate a unique ID for the user activity review
        user_activity_review["user_activity_review_id"] = user_activity_review_id
        # Your logic to create a new user activity review
        return user_activity_review

@blp.route("/<int:user_activity_review_id>")
class UserActivityReviewItem(MethodView):
    @blp.response(status_code=200, schema=UserActivityReviewSchema)
    def get(self, user_activity_review_id):
        # Your logic to fetch a user activity review by ID
        user_activity_review = {}
        return user_activity_review

    @blp.arguments(UpdateUserActivityReviewSchema)
    @blp.response(status_code=200, schema=UserActivityReviewSchema)
    def put(self, payload, user_activity_review_id):
        # Your logic to update a user activity review by ID
        user_activity_review = {}
        return user_activity_review

    @blp.response(status_code=204)
    def delete(self, user_activity_review_id):
        # Your logic to delete a user activity review by ID
        pass
