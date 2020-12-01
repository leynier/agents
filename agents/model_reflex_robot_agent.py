from random import choice
from typing import Dict, Tuple

from agents.cell import Cell
from agents.robot_action import RobotAction
from agents.robot_agent import RobotAgent, RobotDx, RobotDy


class ModelReflexRobotAgent(RobotAgent):
    class Model:
        def __init__(self):
            self.visited: Dict[Tuple[int, int], int] = {}
            self.time: int = 0

    def __init__(self, x, y):
        super(ModelReflexRobotAgent, self).__init__(x, y)
        self.model = ModelReflexRobotAgent.Model()

    def get_random_action(self, environment) -> RobotAction:
        time = -1
        move = None
        for action in [
            RobotAction.MoveNorth,
            RobotAction.MoveEast,
            RobotAction.MoveSouth,
            RobotAction.MoveWest,
        ]:
            row = self.x + RobotDx[action.value - 1]
            column = self.y + RobotDy[action.value - 1]
            if (
                environment.is_valid(row, column)
                and environment.matrix[row][column] != Cell.Obstacle
                and not any(
                    [
                        other.x == row and other.y == column
                        for other in environment.robots
                    ]
                )
            ):
                if (row, column) not in self.model.visited:
                    self.model.visited[row, column] = self.model.time
                    return action
                elif not move:
                    move = action
                    time = self.model.visited[(row, column)]
                elif self.model.visited[(row, column)] < time:
                    move = action
                    time = self.model.visited[(row, column)]
        return choice(
            [
                RobotAction.MoveNorth,
                RobotAction.MoveEast,
                RobotAction.MoveSouth,
                RobotAction.MoveWest,
            ]
        )

    def get_action(self, environment) -> RobotAction:
        self.model.time += 1
        if self.model.time % environment.random_time == 1:
            self.model.visited.clear()
        if self.is_loading():
            if environment.matrix[self.x][self.y] == Cell.Barnyard:
                return RobotAction.DropBaby
            action = self.get_action_by_shortest_cell(environment, Cell.Barnyard)
            if action is not None:
                return action
        if environment.matrix[self.x][self.y] == Cell.Dirty:
            return RobotAction.Clean
        if environment.matrix[self.x][self.y] in [Cell.Free, Cell.Barnyard]:
            return self.get_random_action(environment)
        return RobotAction.Hold
