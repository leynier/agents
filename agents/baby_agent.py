from random import choice
from typing import List, Optional

from agents.agent import Agent
from agents.baby_action import BabyAction
from agents.cell import Cell
from agents.directions import Dx, Dy


class BabyAgent(Agent):
    def __init__(self, x, y):
        super(BabyAgent, self).__init__(x, y)
        self.robot: Optional[Agent] = None

    def is_loaded(self) -> bool:
        return self.robot is not None

    def get_action(self, environment) -> BabyAction:
        if environment.matrix[self.x][self.y] == Cell.Barnyard or self.robot:
            return BabyAction.Hold
        options: List[BabyAction] = [BabyAction.Hold]
        for action in [
            BabyAction.MoveNorth,
            BabyAction.MoveEast,
            BabyAction.MoveSouth,
            BabyAction.MoveWest,
        ]:
            row = self.x + Dx[action.value - 1]
            column = self.y + Dy[action.value - 1]
            if (
                environment.is_valid(row, column)
                and not environment.is_occupied(row, column)
                and environment.matrix[row][column] in [Cell.Free, Cell.Obstacle]
            ):
                options.append(action)
        return choice(options)
