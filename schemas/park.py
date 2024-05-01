from marshmallow import fields, Schema

from schemas.sort import SortByEnum, SortDirectionEnum


class CreateParkSchema(Schema):
    name = fields.String()
    location = fields.String()
    description = fields.String()
    established_date = fields.String()
    size = fields.String()
    website = fields.String()
    entrance_info = fields.String()


class UpdateParkSchema(CreateParkSchema):
    visitor_count = fields.Number()


class ParkSchema(UpdateParkSchema):
    id = fields.UUID()


class ParkListSchema(Schema):
    parks = fields.List(fields.Nested(ParkSchema()))


class ParksParamsSchema(Schema):
    order_by = fields.Enum(SortByEnum, load_default=SortByEnum.established_date)
    order = fields.Enum(SortDirectionEnum, load_default=SortDirectionEnum.asc)

