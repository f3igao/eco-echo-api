from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint

from models.state_model import StateModel
from schemas.state_schema import StatesParamsSchema, StateListSchema, UpdateStateSchema, StateSchema, CreateStateSchema

blp = Blueprint("state", "state", url_prefix="/states", description="State API")


@blp.route("")
class StateCollection(MethodView):
    @blp.arguments(StatesParamsSchema, location="query")
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
