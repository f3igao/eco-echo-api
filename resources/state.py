from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import fields, Schema
from enum import Enum

from mocks.activity_data import activity_data
from models.state_model import StateModel

blp = Blueprint("state", "state", url_prefix="/states", description="State API")


class SortDirectionEnum(str, Enum):
    asc = "asc"
    desc = "desc"


class ActivitiesParamsSchema(Schema):
    order_by = fields.Str(
        description="Field to sort by",
        missing="name"
    )
    order = fields.Enum(SortDirectionEnum, missing=SortDirectionEnum.asc)


class CreateStateSchema(Schema):
    name = fields.Str(required=True)


class UpdateStateSchema(Schema):
    name = fields.Str()


class StateSchema(Schema):
    state_id = fields.Int()
    name = fields.Str()
    region = fields.Str()


class StateListSchema(Schema):
    states = fields.List(fields.Nested(StateSchema()))


@blp.route("")
class StateCollection(MethodView):
    @blp.arguments(ActivitiesParamsSchema, location="query")
    @blp.response(status_code=200, schema=StateListSchema)
    def get(self, params):
        return {"states": StateModel.find_all()}

    @blp.arguments(CreateStateSchema)
    @blp.response(status_code=201, schema=StateSchema)
    def post(self, state):
        # You would typically add a new state to the database here
        # For now, let's return the created state
        state["state_id"] = 3  # Assign a unique ID (assuming ID 3 for the new state)
        return state


@blp.route("/<int:state_id>")
class StateItem(MethodView):
    @blp.response(status_code=200, schema=StateSchema)
    def get(self, state_id):
        # You would typically fetch a state from the database here
        # For now, let's return mock data
        return {"state_id": state_id, "name": f"State {state_id}"}

    @blp.arguments(UpdateStateSchema)
    @blp.response(status_code=200, schema=StateSchema)
    def put(self, payload, state_id):
        # You would typically update a state in the database here
        # For now, let's return the updated state
        return {"state_id": state_id, "name": payload["name"]}

    @blp.response(status_code=204)
    def delete(self, state_id):
        # You would typically delete a state from the database here
        # For now, let's return a successful response
        return
