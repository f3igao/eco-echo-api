import uuid

from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import fields, Schema
from enum import Enum

from mocks.activity_data import activity_data as activities

blp = Blueprint("activity", "activity", url_prefix="/activities", description="Activity API")


class SortDirectionEnum(str, Enum):
    asc = "asc"
    desc = "desc"


class ActivitiesParamsSchema(Schema):
    order_by = fields.Str(
        description="Field to sort by",
        missing="name"
    )
    order = fields.Enum(SortDirectionEnum, missing=SortDirectionEnum.asc)


class CreateActivitySchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    duration = fields.Int(required=True)
    difficulty = fields.Float(required=True)
    require_special_equipment = fields.Boolean(required=True)


class UpdateActivitySchema(Schema):
    name = fields.Str()
    description = fields.Str()
    duration = fields.Int()
    difficulty = fields.Float()
    require_special_equipment = fields.Boolean()


class ActivitySchema(Schema):
    activity_id = fields.Int()
    park_id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    duration = fields.Int()
    difficulty = fields.Float()
    require_special_equipment = fields.Boolean()


class ActivityListSchema(Schema):
    activities = fields.List(fields.Nested(ActivitySchema()))


@blp.route("")
class ActivityCollection(MethodView):
    @blp.arguments(ActivitiesParamsSchema, location="query")
    @blp.response(status_code=200, schema=ActivityListSchema)
    def get(self, params):
        sorted_activities = sorted(activities, key=lambda activity: activity[params["order_by"]],
                                   reverse=params["order"] == SortDirectionEnum.desc)
        return {"activities": sorted_activities}

    @blp.arguments(CreateActivitySchema)
    @blp.response(status_code=201, schema=ActivitySchema)
    def post(self, activity):
        activity["activity_id"] = len(activities) + 1
        activities.append(activity)
        return activity


@blp.route("/<int:activity_id>")
class ActivityItem(MethodView):
    @blp.response(status_code=200, schema=ActivitySchema)
    def get(self, activity_id):
        for activity in activities:
            if activity["activity_id"] == activity_id:
                return activity
        abort(404, message=f"Activity with ID {activity_id} not found")

    @blp.arguments(UpdateActivitySchema)
    @blp.response(status_code=200, schema=ActivitySchema)
    def put(self, payload, activity_id):
        for activity in activities:
            if activity["activity_id"] == activity_id:
                activity.update(payload)
                return activity
        abort(404, message=f"Activity with ID {activity_id} not found")

    @blp.response(status_code=204)
    def delete(self, activity_id):
        for index, activity in enumerate(activities):
            if activity["activity_id"] == activity_id:
                activities.pop(index)
                return

