from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint

from models import ParkModel
from models.activity_model import ActivityModel
from schemas.activity_schema import ActivitiesParamsSchema, ActivitySchema, CreateActivitySchema, UpdateActivitySchema, \
    ActivityListSchema
from schemas.sort_schema import SortDirectionEnum

blp = Blueprint("activity", "activity", url_prefix="/api/activities", description="Activity API")


@blp.route("")
class ActivityCollection(MethodView):
    @blp.response(status_code=200, schema=ActivityListSchema)
    def get(self):
        activities = ActivityModel.find_all()
        return {"activities": activities}

    @blp.arguments(CreateActivitySchema)
    @blp.response(status_code=201, schema=ActivitySchema)
    def post(self, activity_data):
        park_id = activity_data.pop("park_id")  # Remove park_id from activity data
        park = ParkModel.find_by_id(park_id)  # Find the park by park_id
        if not park:
            abort(404, message=f"Park with ID {park_id} not found")

        activity = ActivityModel(
            name=activity_data["name"],
            description=activity_data["description"],
            duration=activity_data["duration"],
            difficulty=activity_data["difficulty"],
            require_special_equipment=activity_data["require_special_equipment"],
            park=park,
            created_at=activity_data.get("created_at"),
            updated_at=activity_data.get("updated_at")
        )
        activity.save_to_db()
        return activity


@blp.route("/<int:activity_id>")
class ActivityItem(MethodView):
    @blp.response(status_code=200, schema=ActivitySchema)
    def get(self, activity_id):
        activity = ActivityModel.find_by_id(activity_id)
        if not activity:
            abort(404, message=f"Activity with ID {activity_id} not found")
        return activity

    @blp.arguments(UpdateActivitySchema)
    @blp.response(status_code=201, schema=ActivitySchema)
    def put(self, payload, activity_id):
        activity = ActivityModel.find_by_id(activity_id)
        if not activity:
            abort(404, message=f"Activity with ID {activity_id} not found")
        activity.update(payload)
        return activity

    @blp.response(status_code=204)
    def delete(self, activity_id):
        activity = ActivityModel.find_by_id(activity_id)
        if not activity:
            abort(404, message=f"Activity with ID {activity_id} not found")
        activity.delete_from_db()
        return
