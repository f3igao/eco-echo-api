from marshmallow import fields, Schema


class CreateFollowSchema(Schema):
    follower_id = fields.Int(required=True)
    following_id = fields.Int(required=True)


class FollowSchema(CreateFollowSchema):
    follow_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


class FollowStatusSchema(Schema):
    is_following = fields.Boolean()


class FollowUserSchema(Schema):
    user_id = fields.Int(dump_only=True)
    name = fields.Str()
    email = fields.Email()
    is_private = fields.Boolean()


class FollowUserListSchema(Schema):
    users = fields.List(fields.Nested(FollowUserSchema()))
    total = fields.Int()
