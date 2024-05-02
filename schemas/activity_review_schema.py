from marshmallow import fields, Schema


class CreateActivityReviewSchema(Schema):
    user_id = fields.Int(required=True)
    rating = fields.Decimal(required=True)
    comment = fields.Str(required=True)
    media_url = fields.Str()
    is_private = fields.Boolean(required=True)


class UpdateActivityReviewSchema(CreateActivityReviewSchema):
    updated_at = fields.DateTime()


class ActivityReviewSchema(UpdateActivityReviewSchema):
    activity_id = fields.Int()
    created_at = fields.DateTime()


class ActivityReviewListSchema(Schema):
    activity_reviews = fields.List(fields.Nested(ActivityReviewSchema()))

