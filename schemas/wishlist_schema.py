from marshmallow import fields, Schema


class CreateWishlistSchema(Schema):
    user_id = fields.Int(required=True)
    park_id = fields.Int(required=True)


class UpdateWishlistSchema(Schema):
    planned_date_start = fields.Date(allow_none=True, load_default=None)
    planned_date_end = fields.Date(allow_none=True, load_default=None)
    notes = fields.Str(allow_none=True, load_default=None)


class WishlistSchema(CreateWishlistSchema):
    wishlist_id = fields.Int()
    created_at = fields.DateTime()
    planned_date_start = fields.Date(allow_none=True)
    planned_date_end = fields.Date(allow_none=True)
    notes = fields.Str(allow_none=True)


class WishlistListSchema(Schema):
    wishlists = fields.List(fields.Nested(WishlistSchema()))
