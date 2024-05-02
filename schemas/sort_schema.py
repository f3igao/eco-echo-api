import enum


class SortByEnum(enum.Enum):
    created_at = "created_at"
    established_date = "established_date"
    name = "name"


class SortDirectionEnum(enum.Enum):
    asc = "asc"
    desc = "desc"
    