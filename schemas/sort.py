import enum


class SortByEnum(enum.Enum):
    task = "task"
    created = "created"
    established_date = "established_date"


class SortDirectionEnum(enum.Enum):
    asc = "asc"
    desc = "desc"
    