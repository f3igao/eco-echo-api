from marshmallow import fields, Schema


class CreateWishlistSchema(Schema):
    user_id = fields.Int(required=True)
    park_id = fields.Int(required=True)


class WishlistSchema(CreateWishlistSchema):
    wishlist_id = fields.Int()
    created_at = fields.DateTime()


class WishlistListSchema(Schema):
    wishlists = fields.List(fields.Nested(WishlistSchema()))
