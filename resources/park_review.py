import uuid
from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint

from models.park_review_model import ParkReviewModel
from schemas.park_review_schema import CreateParkReviewSchema, UpdateParkReviewSchema, ParkReviewSchema, \
    ParkReviewListSchema

blp = Blueprint("park_review", "park_review", url_prefix="/park_reviews", description="Park Review API")


@blp.route("")
class ParkReviewCollection(MethodView):
    @blp.response(status_code=200, schema=ParkReviewListSchema)
    def get(self):
        park_reviews = ParkReviewModel.find_all()
        return {"park_reviews": park_reviews}

    @blp.arguments(CreateParkReviewSchema)
    @blp.response(status_code=201, schema=ParkReviewSchema)
    def post(self, park_review_data):
        park_review = ParkReviewModel(
            park_id=park_review_data["park_id"],
            user_id=park_review_data["user_id"],
            rating=park_review_data["rating"],
            visit_date=park_review_data["visit_date"],
            comment=park_review_data.get("comment"),
            media_url=park_review_data.get("media_url"),
            is_private=park_review_data["is_private"],
            created_at=park_review_data.get("created_at"),
            updated_at=park_review_data.get("updated_at")
        )
        park_review.save_to_db()
        return park_review


@blp.route("/<int:park_review_id>")
class ParkReviewItem(MethodView):
    @blp.response(status_code=200, schema=ParkReviewSchema)
    def get(self, park_review_id):
        park_review = ParkReviewModel.find_by_id(park_review_id)
        if not park_review:
            abort(404, message="Park review not found")
        return park_review

    @blp.arguments(UpdateParkReviewSchema)
    @blp.response(status_code=200, schema=ParkReviewSchema)
    def put(self, payload, park_review_id):
        park_review = ParkReviewModel.find_by_id(park_review_id)
        if not park_review:
            abort(404, message="Park review not found")
        park_review.update_from_dict(payload)
        return park_review

    @blp.response(status_code=204)
    def delete(self, park_review_id):
        park_review = ParkReviewModel.find_by_id(park_review_id)
        if not park_review:
            abort(404, message="Park review not found")
        park_review.delete_from_db()
        return
