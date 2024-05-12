from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint

from models.state_model import StateModel
from schemas.state_schema import CreateStateSchema, UpdateStateSchema, StateSchema, StateListSchema

blp = Blueprint("state", "state", url_prefix="/api/states", description="State API")


@blp.route("")
class StateCollection(MethodView):
    @blp.response(status_code=200, schema=StateListSchema)
    def get(self):
        states = StateModel.query.all()
        return {"states": states}

    @blp.arguments(CreateStateSchema)
    @blp.response(status_code=201, schema=StateSchema)
    def post(self, state_data):
        state = StateModel(
            name=state_data["name"],
            region=state_data["region"],
            abbreviation=state_data["abbreviation"],
            created_at=state_data.get("created_at"),
            updated_at=state_data.get("updated_at")
        )
        state.save_to_db()
        return state


@blp.route("/<int:state_id>")
class StateItem(MethodView):
    @blp.response(status_code=200, schema=StateSchema)
    def get(self, state_id):
        state = StateModel.find_by_id(state_id)
        if not state:
            abort(404, message="State not found")
        return state

    @blp.arguments(UpdateStateSchema)
    @blp.response(status_code=200, schema=StateSchema)
    def put(self, payload, state_id):
        state = StateModel.find_by_id(state_id)
        if not state:
            abort(404, message="State not found")
        state.update_from_dict(payload)
        return state

    @blp.response(status_code=204)
    def delete(self, state_id):
        state = StateModel.find_by_id(state_id)
        if not state:
            abort(404, message="State not found")
        state.delete_from_db()
        return
