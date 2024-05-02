import uuid

from flask.views import MethodView
from flask_smorest import Blueprint

from schemas.activity_review_schema import ActivityReviewListSchema, ActivityReviewSchema, CreateActivityReviewSchema, \
    UpdateActivityReviewSchema

blp = Blueprint("activity_review", "activity_review", url_prefix="/activity_reviews", description="Activity Review API")


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
