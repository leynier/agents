from random import choice
from typing import List, Set, Tuple

from agents.cell import Cell
from agents.robot_action import RobotAction
from agents.robot_agent import RobotAgent, RobotDx, RobotDy
from agents.robot_model import RobotModel


class ModelReflexRobotAgent(RobotAgent):
    def __init__(self, x, y):
        super(ModelReflexRobotAgent, self).__init__(x, y)
        self.model = RobotModel()

    def get_best_action(self, environment, cell: Cell) -> RobotAction:
        queue: List[Tuple[int, int, RobotAction]] = [(self.x, self.y, RobotAction.Hold)]
        visit: Set[Tuple[int, int]] = {(self.x, self.y)}
        while queue:
            ax, ay, fac = queue.pop(0)
            for action in [
                RobotAction.MoveNorth,
                RobotAction.MoveEast,
                RobotAction.MoveSouth,
                RobotAction.MoveWest,
            ]:
                row = ax + RobotDx[action]
                column = ay + RobotDy[action]
                ufac = fac
                if fac == RobotAction.Hold:
                    ufac = action
                if (
                    (row, column) not in visit
                    and environment.is_valid(row, column)
                    and environment.matrix[row][column] != Cell.Obstacle
                    and not any(
                        [
                            robot.x == row and robot.y == column
                            for robot in environment.robots
                        ]
                    )
                    and not (
                        environment.matrix[row][column] == Cell.Barnyard
                        and any(
                            [
                                baby.x == row and baby.y == column
                                for baby in environment.babies
                            ]
                        )
                    )
                ):
                    if environment.matrix[row][column] == cell:
                        return ufac
                    visit.add((row, column))
                    queue.append((row, column, ufac))
            if self.is_loading():
                for action, actions in [
                    (
                        RobotAction.MoveNorth,
                        [
                            RobotAction.MoveNorthWest,
                            RobotAction.MoveNorthEast,
                            RobotAction.FastMoveNorth,
                        ],
                    ),
                    (
                        RobotAction.MoveEast,
                        [
                            RobotAction.MoveNorthEast,
                            RobotAction.MoveSouthEast,
                            RobotAction.FastMoveEast,
                        ],
                    ),
                    (
                        RobotAction.MoveSouth,
                        [
                            RobotAction.MoveSouthEast,
                            RobotAction.MoveSouthWest,
                            RobotAction.FastMoveSouth,
                        ],
                    ),
                    (
                        RobotAction.MoveWest,
                        [
                            RobotAction.MoveSouthWest,
                            RobotAction.MoveNorthWest,
                            RobotAction.FastMoveWest,
                        ],
                    ),
                ]:
                    row = ax + RobotDx[action.value - 1]
                    column = ay + RobotDy[action.value - 1]
                    if (
                        environment.is_valid(row, column)
                        and environment.matrix[row][column] != Cell.Obstacle
                        and not any(
                            [
                                robot.x == row and robot.y == column
                                for robot in environment.robots
                            ]
                        )
                        and not (
                            environment.matrix[row][column] == Cell.Barnyard
                            and any(
                                [
                                    baby.x == row and baby.y == column
                                    for baby in environment.babies
                                ]
                            )
                        )
                    ):
                        for action in actions:
                            row = ax + RobotDx[action.value - 1]
                            column = ay + RobotDy[action.value - 1]
                            ufac = fac
                            if fac == RobotAction.Hold:
                                ufac = action
                            if (
                                (row, column) not in visit
                                and environment.is_valid(row, column)
                                and environment.matrix[row][column] != Cell.Obstacle
                                and not any(
                                    [
                                        robot.x == row and robot.y == column
                                        for robot in environment.robots
                                    ]
                                )
                                and not (
                                    environment.matrix[row][column] == Cell.Barnyard
                                    and any(
                                        [
                                            baby.x == row and baby.y == column
                                            for baby in environment.babies
                                        ]
                                    )
                                )
                            ):
                                if environment.matrix[row][column] == cell:
                                    return ufac
                                visit.add((row, column))
                                queue.append((row, column, ufac))
        return RobotAction.Hold

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
            return self.get_best_action(environment, Cell.Barnyard)
        if environment.matrix[self.x][self.y] == Cell.Dirty:
            return RobotAction.Clean
        if environment.matrix[self.x][self.y] in [Cell.Free, Cell.Barnyard]:
            return self.get_random_action(environment)
        return RobotAction.Hold
