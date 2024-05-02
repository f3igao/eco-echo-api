from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint

from models.activity_model import ActivityModel
from schemas.activity_schema import ActivitiesParamsSchema, ActivitySchema, CreateActivitySchema, UpdateActivitySchema, \
    ActivityListSchema

blp = Blueprint("activity", "activity", url_prefix="/activities", description="Activity API")


@blp.route("")
class ActivityCollection(MethodView):
    @blp.arguments(ActivitiesParamsSchema, location="query")
    @blp.response(status_code=200, schema=ActivityListSchema)
    def get(self, params):
        activities = ActivityModel.find_all()
        return {"activities": activities}

    @blp.arguments(CreateActivitySchema)
    @blp.response(status_code=201, schema=ActivitySchema)
    def post(self, activity):
        new_activity = ActivityModel(**activity)
        new_activity.save_to_db()
        return new_activity.json(), 201


@blp.route("/<int:activity_id>")
class ActivityItem(MethodView):
    @blp.response(status_code=200, schema=ActivitySchema)
    def get(self, activity_id):
        activity = ActivityModel.find_by_id(activity_id)
        if not activity:
            abort(404, message=f"Activity with ID {activity_id} not found")
        return activity.json()

    @blp.arguments(UpdateActivitySchema)
    @blp.response(status_code=201, schema=ActivitySchema)
    def put(self, payload, activity_id):
        activity = ActivityModel.find_by_id(activity_id)
        if not activity:
            abort(404, message=f"Activity with ID {activity_id} not found")
        activity.update(payload)
        return activity.json()

    @blp.response(status_code=204)
    def delete(self, activity_id):
        activity = ActivityModel.find_by_id(activity_id)
        if not activity:
            abort(404, message=f"Activity with ID {activity_id} not found")
        activity.delete_from_db()
        return
