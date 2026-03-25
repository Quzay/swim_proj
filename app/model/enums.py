import enum


class Stroke_type(str, enum.Enum):
    FREESTYLE = "Freestyle"
    BACKSTROKE = "Backstroke"
    BREASTSTROKE = "Breaststroke"
    BUTTERFLY = "Butterfly"

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class Challenge_status(str, enum.Enum):
    ACTIVE = "active"
    FAILURE = "failure"
    COMPLETED = "completed"