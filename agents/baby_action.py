from enum import IntEnum, auto


class BabyAction(IntEnum):
    MoveNorth = auto()
    MoveEast = auto()
    MoveSouth = auto()
    MoveWest = auto()
    Hold = auto()
