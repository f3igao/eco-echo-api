from flask import abort, request
from flask.views import MethodView
from flask_smorest import Blueprint

from models.wishlist_model import WishlistModel
from models.park_model import ParkModel
from models.user_model import UserModel
from schemas.wishlist_schema import CreateWishlistSchema, UpdateWishlistSchema, WishlistSchema, WishlistListSchema

blp = Blueprint("wishlist", "wishlist", url_prefix="/api/wishlists", description="Wishlist API")


@blp.route("")
class WishlistCollection(MethodView):
    @blp.response(status_code=200, schema=WishlistListSchema)
    def get(self):
        user_id = request.args.get("user_id", type=int)
        if user_id is not None:
            wishlists = WishlistModel.find_by_user_id(user_id)
        else:
            wishlists = WishlistModel.query.order_by(WishlistModel.created_at.desc()).all()
        return {"wishlists": wishlists}

    @blp.arguments(CreateWishlistSchema)
    @blp.response(status_code=201, schema=WishlistSchema)
    def post(self, wishlist_data):
        user_id = wishlist_data["user_id"]
        park_id = wishlist_data["park_id"]

        if not UserModel.find_by_id(user_id):
            abort(404, message=f"User with ID {user_id} not found")
        if not ParkModel.find_by_id(park_id):
            abort(404, message=f"Park with ID {park_id} not found")

        existing = WishlistModel.find_by_user_and_park(user_id, park_id)
        if existing:
            abort(409, message="This park is already in your wishlist")

        wishlist = WishlistModel(user_id=user_id, park_id=park_id)
        wishlist.save_to_db()
        return wishlist


@blp.route("/<int:wishlist_id>")
class WishlistItem(MethodView):
    @blp.response(status_code=200, schema=WishlistSchema)
    def get(self, wishlist_id):
        wishlist = WishlistModel.find_by_id(wishlist_id)
        if not wishlist:
            abort(404, message="Wishlist entry not found")
        return wishlist

    @blp.arguments(UpdateWishlistSchema)
    @blp.response(status_code=200, schema=WishlistSchema)
    def patch(self, update_data, wishlist_id):
        wishlist = WishlistModel.find_by_id(wishlist_id)
        if not wishlist:
            abort(404, message="Wishlist entry not found")
        wishlist.planned_date_start = update_data.get("planned_date_start")
        wishlist.planned_date_end = update_data.get("planned_date_end")
        wishlist.notes = update_data.get("notes")
        wishlist.save_to_db()
        return wishlist

    @blp.response(status_code=204)
    def delete(self, wishlist_id):
        wishlist = WishlistModel.find_by_id(wishlist_id)
        if not wishlist:
            abort(404, message="Wishlist entry not found")
        wishlist.delete_from_db()
        return


@blp.route("/user/<int:user_id>")
class WishlistByUser(MethodView):
    @blp.response(status_code=200, schema=WishlistListSchema)
    def get(self, user_id):
        if not UserModel.find_by_id(user_id):
            abort(404, message=f"User with ID {user_id} not found")
        wishlists = WishlistModel.find_by_user_id(user_id)
        return {"wishlists": wishlists}


@blp.route("/user/<int:user_id>/park/<int:park_id>")
class WishlistByUserAndPark(MethodView):
    @blp.response(status_code=204)
    def delete(self, user_id, park_id):
        wishlist = WishlistModel.find_by_user_and_park(user_id, park_id)
        if not wishlist:
            abort(404, message="Wishlist entry not found")
        wishlist.delete_from_db()
        return
