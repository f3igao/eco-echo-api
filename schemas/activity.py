from marshmallow import fields, Schema

from schemas.sort import SortByEnum, SortDirectionEnum


class CreateActivitySchema(Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)
    duration = fields.Integer(required=True)
    difficulty = fields.Float(required=True)
    require_special_equipment = fields.Boolean(required=True)


class UpdateActivitySchema(CreateActivitySchema):
    pass  # No additional fields for updating activity


class ActivitySchema(UpdateActivitySchema):
    activity_id = fields.Integer()
    park_id = fields.Integer()


class ActivityListSchema(Schema):
    activities = fields.List(fields.Nested(ActivitySchema()))


class ActivitiesParamsSchema(Schema):
    order_by = fields.Enum(SortByEnum, by_value=True, missing=SortByEnum.name)
    order = fields.Enum(SortDirectionEnum, by_value=True, missing=SortDirectionEnum.asc)
