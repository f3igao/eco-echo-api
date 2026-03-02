from marshmallow import fields, Schema


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class CreateUserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class UpdateUserSchema(Schema):
    name = fields.Str(load_default=None)
    email = fields.Email(load_default=None)
    password = fields.Str(load_default=None)
    is_private = fields.Boolean(load_default=None)


class UserSchema(Schema):
    user_id = fields.Int(dump_only=True)
    name = fields.Str()
    email = fields.Email()
    is_private = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UserDetailSchema(UserSchema):
    follower_count = fields.Int(dump_only=True)
    following_count = fields.Int(dump_only=True)


class UserListSchema(Schema):
    users = fields.List(fields.Nested(UserSchema()))
