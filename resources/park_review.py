import uuid
from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import fields, Schema

from schemas.park_review_schema import ParkReviewSchema, CreateParkReviewSchema, ParkReviewListSchema, \
    UpdateParkReviewSchema

blp = Blueprint("park_review", "park_review", url_prefix="/park_reviews", description="Park Review API")


@blp.route("")
class ParkReviewCollection(MethodView):
    @blp.response(status_code=200, schema=ParkReviewListSchema)
    def get(self):
        # Your logic to fetch park reviews
        park_reviews = []
        return {"park_reviews": park_reviews}

    @blp.arguments(CreateParkReviewSchema)
    @blp.response(status_code=201, schema=ParkReviewSchema)
    def post(self, park_review):
        park_review_id = uuid.uuid4().int  # Generate a unique ID for the park review
        park_review["park_review_id"] = park_review_id
        # Your logic to create a new park review
        return park_review


@blp.route("/<int:park_review_id>")
class ParkReviewItem(MethodView):
    @blp.response(status_code=200, schema=ParkReviewSchema)
    def get(self, park_review_id):
        # Your logic to fetch a park review by ID
        park_review = {}
        return park_review

    @blp.arguments(UpdateParkReviewSchema)
    @blp.response(status_code=200, schema=ParkReviewSchema)
    def put(self, payload, park_review_id):
        # Your logic to update a park review by ID
        park_review = {}
        return park_review

    @blp.response(status_code=204)
    def delete(self, park_review_id):
        # Your logic to delete a park review by ID
        pass
