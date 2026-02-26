from marshmallow import fields, Schema


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class CreateUserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class UpdateUserSchema(CreateUserSchema):
    updated_at = fields.DateTime()


class UserSchema(UpdateUserSchema):
    user_id = fields.Int()
    created_at = fields.DateTime()


class UserListSchema(Schema):
    users = fields.List(fields.Nested(UserSchema()))
