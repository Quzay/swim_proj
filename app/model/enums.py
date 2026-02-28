import enum


class Stroke_type(enum.Enum):
    FREESTYLE = "Freestyle"
    BACKSTROKE = "Backstroke"
    BREASTSTROKE = "Breaststroke"
    BUTTERFLY = "Butterfly"

class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"