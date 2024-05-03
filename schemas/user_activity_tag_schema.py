from marshmallow import fields, Schema


class CreateUserActivityTagSchema(Schema):
    user_id = fields.Int(required=True)
    activity_review_id = fields.Int(required=True)


class UpdateUserActivityTagSchema(CreateUserActivityTagSchema):
    updated_at = fields.DateTime()


class UserActivityTagSchema(UpdateUserActivityTagSchema):
    user_activity_tag_id = fields.Int()
    created_at = fields.DateTime()


class UserActivityTagListSchema(Schema):
    user_activity_tags = fields.List(fields.Nested(UserActivityTagSchema()))
