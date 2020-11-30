from enum import Enum


class Cell(str, Enum):
    Free = "free"
    Dirty = "dirty"
    Barnyard = "barnyard"
    Obstacle = "obstacle"
