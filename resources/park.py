import uuid

from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from schemas.park import ParksParamsSchema, CreateParkSchema, ParkSchema, ParkListSchema, UpdateParkSchema
from schemas.sort import  SortDirectionEnum

from mocks.park_data import park_data as parks

blp = Blueprint("park", "park", url_prefix="/", description="Park API")


@blp.route("/parks")
class TodoCollection(MethodView):
    @blp.arguments(ParksParamsSchema, location="query")
    @blp.response(status_code=200, schema=ParkListSchema)
    def get(self, params):
        sorted_parks = sorted(parks, key=lambda park: park[params["order_by"].value], reverse=params["order"] == SortDirectionEnum.desc)
        return {"parks": sorted_parks}

    @blp.arguments(CreateParkSchema)
    @blp.response(status_code=201, schema=ParkSchema)
    def post(self, park):
        park["id"] = uuid.uuid4()
        # park["location"] =
        # park["description"] =
        # park["established_date"] =
        # park["size"] =
        # park["visitor_count"] =
        # park["website"] =
        # park["entrance_info"] =
        print("new park:", park)
        parks.append(park)
        return park


@blp.route("/parks/<uuid:park_id>")
class TodoPark(MethodView):
    @blp.response(status_code=200, schema=ParkSchema)
    def get(self, park_id):
        for park in parks:
            if park["id"] == park_id:
                return park
        abort(404, message=f"Park with id {park_id} not found")

    @blp.arguments(UpdateParkSchema)
    @blp.response(status_code=200, schema=ParkSchema)
    def put(self, payload, park_id):
        for park in parks:
            if park["id"] == park_id:
                park["completed"] = payload["completed"]
                park["park"] = payload["park"]
                return park
        abort(404, message=f"Park with id {park_id} not found")

    @blp.response(status_code=204)
    def delete(self, park_id):
        for index, park in enumerate(parks):
            if park["id"] == park_id:
                parks.pop(index)
                return
        abort(404, message=f"Park with id {park_id} not found")
