from flask import abort
from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint

from models import ParkModel
from schemas.park_schema import CreateParkSchema, ParkSchema, ParkListSchema, UpdateParkSchema

blp = Blueprint("park", "park", url_prefix="/api/parks", description="Park API")


@blp.route("")
class ParkCollection(MethodView):
    @blp.response(status_code=200, schema=ParkListSchema)
    def get(self):
        parks = ParkModel.find_all()
        return {"parks": parks}

    @blp.arguments(CreateParkSchema)
    @blp.response(status_code=201, schema=ParkSchema)
    def post(self, park):
        new_park = ParkModel(**park)
        new_park.save_to_db()
        return new_park.json(), 201


@blp.route("/parks/<int:park_id>")
class Park(MethodView):
    @blp.response(status_code=200, schema=ParkSchema)
    def get(self, park_id):
        park = ParkModel.find_by_id(park_id)
        if not park:
            abort(404, message=f"Park with id {park_id} not found")
        return park.json()

    @blp.arguments(UpdateParkSchema)
    @blp.response(status_code=200, schema=ParkSchema)
    def put(self, payload, park_id):
        park = ParkModel.find_by_id(park_id)
        if not park:
            abort(404, message=f"Park with id {park_id} not found")
        park.update(payload)
        return park.json()

    @blp.response(status_code=204)
    def delete(self, park_id):
        park = ParkModel.find_by_id(park_id)
        if not park:
            abort(404, message=f"Park with id {park_id} not found")
        park.delete_from_db()
        return
