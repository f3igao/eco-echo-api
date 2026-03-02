from flask import abort, request
from flask.views import MethodView
from flask_smorest import Blueprint

from models.follow_model import FollowModel
from models.park_review_model import ParkReviewModel
from models.user_model import UserModel
from schemas.park_review_schema import CreateParkReviewSchema, UpdateParkReviewSchema, ParkReviewSchema, \
    ParkReviewListSchema

blp = Blueprint("park-review", "park-review", url_prefix="/api/park-reviews", description="Park Review API")


def _is_review_visible_on_park_page(review, requester_id):
    """Park-page visibility: account privacy is irrelevant (Instagram model).
    Only the review's own is_private flag matters — a privately-marked review
    is only shown to its author."""
    if review.is_private:
        return requester_id is not None and requester_id == review.user_id
    return True


def _is_review_visible_on_profile(review, requester_id):
    """Profile-page visibility: respects both the review's is_private flag and
    the reviewer's account privacy setting."""
    if review.is_private:
        return requester_id is not None and requester_id == review.user_id

    reviewer = UserModel.find_by_id(review.user_id)
    if reviewer and reviewer.is_private:
        if requester_id is None:
            return False
        if requester_id == review.user_id:
            return True
        return FollowModel.find_by_ids(requester_id, review.user_id) is not None

    return True


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
            activities=park_review_data.get("activities"),
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


@blp.route("/park/<int:park_id>")
class ParkReviewByPark(MethodView):
    @blp.response(status_code=200, schema=ParkReviewListSchema)
    def get(self, park_id):
        requester_id = request.args.get("requester_id", type=int)
        all_reviews = ParkReviewModel.find_by_park_id(park_id)
        visible = [r for r in all_reviews if _is_review_visible_on_park_page(r, requester_id)]
        return {"park_reviews": visible}


@blp.route("/user/<int:user_id>")
class ParkReviewByUser(MethodView):
    @blp.response(status_code=200, schema=ParkReviewListSchema)
    def get(self, user_id):
        requester_id = request.args.get("requester_id", type=int)
        target_user = UserModel.find_by_id(user_id)
        if not target_user:
            abort(404, message="User not found")

        if target_user.is_private:
            if requester_id is None or (
                requester_id != user_id and not FollowModel.find_by_ids(requester_id, user_id)
            ):
                abort(403, message="This account is private")

        reviews = ParkReviewModel.find_by_user_id(user_id)
        if requester_id != user_id:
            reviews = [r for r in reviews if not r.is_private]
        return {"park_reviews": reviews}
