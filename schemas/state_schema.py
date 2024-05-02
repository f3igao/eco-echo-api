from marshmallow import Schema, fields

from schemas.sort_schema import SortDirectionEnum, SortByEnum


class StatesParamsSchema(Schema):
    order_by = fields.Enum(SortByEnum, load_default=SortByEnum.name)
    order = fields.Enum(SortDirectionEnum, load_default=SortDirectionEnum.asc)


class CreateStateSchema(Schema):
    name = fields.Str(required=True)
    region = fields.Str(required=True)
    abbreviation = fields.Str(required=True)


class UpdateStateSchema(CreateStateSchema):
    updated_at = fields.DateTime()



class StateSchema(UpdateStateSchema):
    state_id = fields.Int()
    created_at = fields.DateTime()


class StateListSchema(Schema):
    states = fields.List(fields.Nested(StateSchema()))

