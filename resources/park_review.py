import uuid
from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import fields, Schema

blp = Blueprint("park_review", "park_review", url_prefix="/park_reviews", description="Park Review API")

class CreateParkReviewSchema(Schema):
    park_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    rating = fields.Decimal(required=True)
    visit_date = fields.Date(required=True)
    comment = fields.Str(required=True)
    media_url = fields.Str()
    is_private = fields.Boolean(required=True)
    timestamp = fields.DateTime(required=True)
    last_modified = fields.DateTime(required=True)

class UpdateParkReviewSchema(Schema):
    park_id = fields.Int()
    user_id = fields.Int()
    rating = fields.Decimal()
    visit_date = fields.Date()
    comment = fields.Str()
    media_url = fields.Str()
    is_private = fields.Boolean()
    timestamp = fields.DateTime()
    last_modified = fields.DateTime()

class ParkReviewSchema(Schema):
    park_review_id = fields.Int()
    park_id = fields.Int()
    user_id = fields.Int()
    rating = fields.Decimal()
    visit_date = fields.Date()
    comment = fields.Str()
    media_url = fields.Str()
    is_private = fields.Boolean()
    timestamp = fields.DateTime()
    last_modified = fields.DateTime()

class ParkReviewListSchema(Schema):
    park_reviews = fields.List(fields.Nested(ParkReviewSchema()))

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
