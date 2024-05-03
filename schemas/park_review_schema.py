from marshmallow import fields, Schema


class CreateParkReviewSchema(Schema):
    park_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    rating = fields.Decimal(required=True)
    visit_date = fields.Date(required=True)
    comment = fields.Str(required=True)
    media_url = fields.Str()
    is_private = fields.Boolean(required=True)


class UpdateParkReviewSchema(CreateParkReviewSchema):
    updated_at = fields.DateTime()


class ParkReviewSchema(UpdateParkReviewSchema):
    park_review_id = fields.Int()


class ParkReviewListSchema(Schema):
    park_reviews = fields.List(fields.Nested(ParkReviewSchema()))

