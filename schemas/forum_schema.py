from marshmallow import fields, Schema


class CreateForumPostSchema(Schema):
    user_id = fields.Int(required=True)
    title = fields.Str(required=True)
    body = fields.Str(required=True)
    park_id = fields.Int(allow_none=True, load_default=None)


class ForumPostSchema(Schema):
    post_id = fields.Int(dump_only=True)
    user_id = fields.Int()
    user_name = fields.Str(dump_only=True)
    park_id = fields.Int(allow_none=True)
    park_name = fields.Str(dump_only=True, allow_none=True)
    title = fields.Str()
    body = fields.Str()
    comment_count = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ForumPostListSchema(Schema):
    posts = fields.List(fields.Nested(ForumPostSchema()))
    total = fields.Int()


class CreateForumCommentSchema(Schema):
    user_id = fields.Int(required=True)
    body = fields.Str(required=True)


class ForumCommentSchema(Schema):
    comment_id = fields.Int(dump_only=True)
    post_id = fields.Int(dump_only=True)
    user_id = fields.Int()
    user_name = fields.Str(dump_only=True)
    body = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ForumPostDetailSchema(ForumPostSchema):
    comments = fields.List(fields.Nested(ForumCommentSchema()), dump_only=True)
