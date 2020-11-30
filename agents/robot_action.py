from enum import IntEnum, auto


class RobotAction(IntEnum):
    MoveNorth = auto()
    MoveEast = auto()
    MoveSouth = auto()
    MoveWest = auto()
    Hold = auto()
    Clean = auto()
    DropBaby = auto()
    MoveSouthEast = auto()
    MoveNorthWest = auto()
    MoveNorthEast = auto()
    MoveSouthWest = auto()
    FastMoveNorth = auto()
    FastMoveEast = auto()
    FastMoveSouth = auto()
    FastMoveWest = auto()
