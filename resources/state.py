from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import fields, Schema
from enum import Enum
from models.state_model import StateModel
from schemas.sort import SortDirectionEnum

blp = Blueprint("state", "state", url_prefix="/states", description="State API")


class ActivitiesParamsSchema(Schema):
    order_by = fields.Str(
        description="Field to sort by",
        missing="name"
    )
    order = fields.Enum(SortDirectionEnum, missing=SortDirectionEnum.asc)


class CreateStateSchema(Schema):
    name = fields.Str(required=True)
    region = fields.Str(required=True)
    abbreviation = fields.Str(required=True)


class UpdateStateSchema(Schema):
    name = fields.Str()
    region = fields.Str()
    abbreviation = fields.Str()


class StateSchema(Schema):
    state_id = fields.Int()
    name = fields.Str()
    region = fields.Str()
    abbreviation = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class StateListSchema(Schema):
    states = fields.List(fields.Nested(StateSchema()))


@blp.route("")
class StateCollection(MethodView):
    @blp.arguments(ActivitiesParamsSchema, location="query")
    @blp.response(status_code=200, schema=StateListSchema)
    def get(self, params):
        states = StateModel.find_all()
        return {"states": states}

    @blp.arguments(CreateStateSchema)
    @blp.response(status_code=201, schema=StateSchema)
    def post(self, state):
        # Assuming you have logic to create a new state in your application
        # For now, let's return the created state
        new_state = StateModel(**state)
        new_state.save_to_db()
        return new_state.json(), 201


@blp.route("/<int:state_id>")
class StateItem(MethodView):
    @blp.response(status_code=200, schema=StateSchema)
    def get(self, state_id):
        state = StateModel.find_by_id(state_id)
        if not state:
            abort(404, message=f"State with ID {state_id} not found")
        return state.json()

    @blp.arguments(UpdateStateSchema)
    @blp.response(status_code=200, schema=StateSchema)
    def put(self, payload, state_id):
        state = StateModel.find_by_id(state_id)
        if not state:
            abort(404, message=f"State with ID {state_id} not found")
        state.update(payload)
        return state.json()

    @blp.response(status_code=204)
    def delete(self, state_id):
        state = StateModel.find_by_id(state_id)
        if not state:
            abort(404, message=f"State with ID {state_id} not found")
        state.delete_from_db()
        return
