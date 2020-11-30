from typing import Dict, Tuple


class RobotModel:
    def __init__(self):
        self.visited: Dict[Tuple[int, int], int] = {}
        self.time: int = 0
