from random import choice
from typing import List

from agents.cell import Cell
from agents.robot_action import RobotAction
from agents.robot_agent import RobotAgent


class RandomRobotAgent(RobotAgent):
    def __init__(self, x, y):
        super(RandomRobotAgent, self).__init__(x, y)

    def get_random_action(self, environment) -> RobotAction:
        moves_dx = [-1, 0, 1, 0, 1, -1, -1, 1]
        moves_dy = [0, 1, 0, -1, 1, -1, 1, -1]
        actions = [
            RobotAction.MoveNorth,
            RobotAction.MoveEast,
            RobotAction.MoveSouth,
            RobotAction.MoveWest,
            RobotAction.MoveSouthEast,
            RobotAction.MoveNorthWest,
            RobotAction.MoveNorthEast,
            RobotAction.MoveSouthWest,
        ]
        options: List[RobotAction] = [RobotAction.Hold]
        for index, (dx, dy) in enumerate(zip(moves_dx, moves_dy)):
            ax = self.x + dx
            ay = self.y + dy
            if (
                environment.is_valid(ax, ay)
                and environment.matrix[ax][ay] != Cell.Obstacle
                and not environment.is_occupied(ax, ay)
            ):
                options.append(actions[index])
        return choice(options)

    def get_action(self, environment) -> RobotAction:
        if self.is_loading():
            if environment.matrix[self.x][self.y] == Cell.Barnyard:
                return RobotAction.DropBaby
        if environment.matrix[self.x][self.y] == Cell.Dirty:
            return RobotAction.Clean
        return self.get_random_action(environment)
