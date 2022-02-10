import enum


class StatusRequest(enum.Enum):
    pending = 0
    failed = 1
    done = 2
