from marshmallow import fields, Schema

from schemas.sort_schema import SortByEnum, SortDirectionEnum


class ActivitiesParamsSchema(Schema):
    order_by = fields.Enum(SortByEnum, load_default=SortByEnum.name)
    order = fields.Enum(SortDirectionEnum, load_default=SortDirectionEnum.asc)


class CreateActivitySchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    duration = fields.Int(required=True)
    difficulty = fields.Float(required=True)
    require_special_equipment = fields.Boolean(required=True)


class UpdateActivitySchema(CreateActivitySchema):
    updated_at = fields.DateTime()


class ActivitySchema(UpdateActivitySchema):
    activity_id = fields.UUID()
    park_id = fields.Integer()
    created_at = fields.DateTime()


class ActivityListSchema(Schema):
    activities = fields.List(fields.Nested(ActivitySchema()))

