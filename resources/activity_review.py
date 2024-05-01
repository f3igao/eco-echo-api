import uuid
from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import fields, Schema

blp = Blueprint("activity_review", "activity_review", url_prefix="/activity_reviews", description="Activity Review API")

class CreateActivityReviewSchema(Schema):
    activity_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    rating = fields.Decimal(required=True)
    comment = fields.Str(required=True)
    media_url = fields.Str()
    is_private = fields.Boolean(required=True)
    timestamp = fields.DateTime(required=True)
    last_modified = fields.DateTime(required=True)

class UpdateActivityReviewSchema(Schema):
    activity_id = fields.Int()
    user_id = fields.Int()
    rating = fields.Decimal()
    comment = fields.Str()
    media_url = fields.Str()
    is_private = fields.Boolean()
    timestamp = fields.DateTime()
    last_modified = fields.DateTime()

class ActivityReviewSchema(Schema):
    activity_review_id = fields.Int()
    activity_id = fields.Int()
    user_id = fields.Int()
    rating = fields.Decimal()
    comment = fields.Str()
    media_url = fields.Str()
    is_private = fields.Boolean()
    timestamp = fields.DateTime()
    last_modified = fields.DateTime()

class ActivityReviewListSchema(Schema):
    activity_reviews = fields.List(fields.Nested(ActivityReviewSchema()))

@blp.route("")
class ActivityReviewCollection(MethodView):
    @blp.response(status_code=200, schema=ActivityReviewListSchema)
    def get(self):
        # Your logic to fetch activity reviews
        activity_reviews = []
        return {"activity_reviews": activity_reviews}

    @blp.arguments(CreateActivityReviewSchema)
    @blp.response(status_code=201, schema=ActivityReviewSchema)
    def post(self, activity_review):
        activity_review_id = uuid.uuid4().int  # Generate a unique ID for the activity review
        activity_review["activity_review_id"] = activity_review_id
        # Your logic to create a new activity review
        return activity_review

@blp.route("/<int:activity_review_id>")
class ActivityReviewItem(MethodView):
    @blp.response(status_code=200, schema=ActivityReviewSchema)
    def get(self, activity_review_id):
        # Your logic to fetch an activity review by ID
        activity_review = {}
        return activity_review

    @blp.arguments(UpdateActivityReviewSchema)
    @blp.response(status_code=200, schema=ActivityReviewSchema)
    def put(self, payload, activity_review_id):
        # Your logic to update an activity review by ID
        activity_review = {}
        return activity_review

    @blp.response(status_code=204)
    def delete(self, activity_review_id):
        # Your logic to delete an activity review by ID
        pass
