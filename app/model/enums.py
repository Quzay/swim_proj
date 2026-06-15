import enum


class Stroke_type(str, enum.Enum):
    FREESTYLE = "Freestyle"
    BACKSTROKE = "Backstroke"
    BREASTSTROKE = "Breaststroke"
    BUTTERFLY = "Butterfly"
    MIXED = "Mixed"

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class Status(str, enum.Enum):
    ACTIVE = "ACTIVE"
    FAILURE = "FAILURE"
    COMPLETED = "COMPLETED"

class ModelName(str, enum.Enum):
    CHALLENGE = "CHALLENGE"
    GOAL = "GOAL"

class Equipment_type(str, enum.Enum):
    FLIPPERS = "FLIPPERS"
    HAND_PADDLES = "HAND_PADDLES"
    SNORKEL = "SNORKEL"