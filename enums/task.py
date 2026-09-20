from enum import Enum

class TaskShortField(str, Enum):
    created_at = "created_at"
    title = "title"
    is_completed = "is_completed"

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc" 