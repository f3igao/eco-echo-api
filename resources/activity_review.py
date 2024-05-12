from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint

from models.activity_review_model import ActivityReviewModel
from schemas.activity_review_schema import CreateActivityReviewSchema, UpdateActivityReviewSchema, ActivityReviewSchema, \
    ActivityReviewListSchema

blp = Blueprint("activity_review", "activity_review", url_prefix="/api/activity_reviews",
                description="Activity Review API")


@blp.route("")
class ActivityReviewCollection(MethodView):
    @blp.response(status_code=200, schema=ActivityReviewListSchema)
    def get(self):
        activity_reviews = ActivityReviewModel.find_all()
        return {"activity_reviews": activity_reviews}

    @blp.arguments(CreateActivityReviewSchema)
    @blp.response(status_code=201, schema=ActivityReviewSchema)
    def post(self, activity_review_data):
        activity_review = ActivityReviewModel(
            activity_id=activity_review_data["activity_id"],
            user_id=activity_review_data["user_id"],
            rating=activity_review_data["rating"],
            comment=activity_review_data.get("comment"),
            media_url=activity_review_data.get("media_url"),
            is_private=activity_review_data["is_private"],
            created_at=activity_review_data.get("created_at"),
            updated_at=activity_review_data.get("updated_at")
        )
        activity_review.save_to_db()
        return activity_review


@blp.route("/<int:activity_review_id>")
class ActivityReviewItem(MethodView):
    @blp.response(status_code=200, schema=ActivityReviewSchema)
    def get(self, activity_review_id):
        activity_review = ActivityReviewModel.find_by_id(activity_review_id)
        if not activity_review:
            abort(404, message="Activity review not found")
        return activity_review

    @blp.arguments(UpdateActivityReviewSchema)
    @blp.response(status_code=200, schema=ActivityReviewSchema)
    def put(self, payload, activity_review_id):
        activity_review = ActivityReviewModel.find_by_id(activity_review_id)
        if not activity_review:
            abort(404, message="Activity review not found")
        activity_review.update_from_dict(payload)
        return activity_review

    @blp.response(status_code=204)
    def delete(self, activity_review_id):
        activity_review = ActivityReviewModel.find_by_id(activity_review_id)
        if not activity_review:
            abort(404, message="Activity review not found")
        activity_review.delete_from_db()
        return
