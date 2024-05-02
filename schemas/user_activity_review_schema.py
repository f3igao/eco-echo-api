from marshmallow import fields, Schema


class CreateUserActivityReviewSchema(Schema):
    user_id = fields.Int(required=True)
    activity_review_id = fields.Int(required=True)
    rating = fields.Decimal(required=True)


class UpdateUserActivityReviewSchema(CreateUserActivityReviewSchema):
    updated_at = fields.DateTime()


class UserActivityReviewSchema(UpdateUserActivityReviewSchema):
    user_activity_review_id = fields.Int()
    created_at = fields.DateTime()


class UserActivityReviewListSchema(Schema):
    user_activity_reviews = fields.List(fields.Nested(UserActivityReviewSchema()))

