import math
from typing import List, Optional, Tuple

from agents.agent import Agent
from agents.cell import Cell
from agents.dijkstra import Dijkstra
from agents.robot_action import RobotAction

RobotDx = [-1, 0, 1, 0, 0, 0, 0, 1, -1, -1, 1, -2, 0, 2, 0]
RobotDy = [0, 1, 0, -1, 0, 0, 0, 1, -1, 1, -1, 0, 2, 0, -2]


class RobotAgent(Agent):
    def __init__(self, x, y):
        super(RobotAgent, self).__init__(x, y)
        self.baby: Optional[Agent] = None

    def is_loading(self) -> bool:
        return self.baby is not None

    def get_action_by_shortest_cell(
        self, environment, cell_target: Cell
    ) -> Optional[RobotAction]:
        dijkstra = Dijkstra(environment, (self.x, self.y))
        cells: List[Tuple[int, int]] = []
        for i, row in enumerate(environment.matrix):
            for j, cell in enumerate(row):
                if cell == cell_target:
                    cells.append((i, j))
        distances = [
            (dijkstra.get_distance(cell), cell)
            for cell in cells
            if dijkstra.get_distance(cell) != math.inf
        ]
        distances.sort()
        if distances:
            best_cell = distances[0][1]
            path = dijkstra.get_path(best_cell)
            if len(path) < 2:
                return None
            ax, ay = (path[1][0] - path[0][0], path[1][1] - path[0][1])
            MoveDx = [-1, 0, 1, 0, 1, -1, -1, 1, -2, 0, 2, 0]
            MoveDy = [0, 1, 0, -1, 1, -1, 1, -1, 0, 2, 0, -2]
            actions = [
                RobotAction.MoveNorth,
                RobotAction.MoveEast,
                RobotAction.MoveSouth,
                RobotAction.MoveWest,
                RobotAction.MoveSouthEast,
                RobotAction.MoveNorthWest,
                RobotAction.MoveNorthEast,
                RobotAction.MoveSouthWest,
                RobotAction.FastMoveNorth,
                RobotAction.FastMoveEast,
                RobotAction.FastMoveSouth,
                RobotAction.FastMoveWest,
            ]
            for index, (mx, my) in enumerate(zip(MoveDx, MoveDy)):
                if ax == mx and ay == my:
                    return actions[index]

    def get_action_by_baby_cell(self, environment) -> Optional[RobotAction]:
        dijkstra = Dijkstra(environment, (self.x, self.y))
        cells: List[Tuple[int, int]] = []
        for i, row in enumerate(environment.matrix):
            for j, _ in enumerate(row):
                if any([baby.x == i and baby.y == j for baby in environment.babies]):
                    cells.append((i, j))
        distances = [
            (dijkstra.get_distance(cell), cell)
            for cell in cells
            if dijkstra.get_distance(cell) != math.inf
        ]
        distances.sort()
        if distances:
            best_cell = distances[0][1]
            path = dijkstra.get_path(best_cell)
            ax, ay = (path[1][0] - path[0][0], path[1][1] - path[0][1])
            MoveDx = [-1, 0, 1, 0, 1, -1, -1, 1, -2, 0, 2, 0]
            MoveDy = [0, 1, 0, -1, 1, -1, 1, -1, 0, 2, 0, -2]
            actions = [
                RobotAction.MoveNorth,
                RobotAction.MoveEast,
                RobotAction.MoveSouth,
                RobotAction.MoveWest,
                RobotAction.MoveSouthEast,
                RobotAction.MoveNorthWest,
                RobotAction.MoveNorthEast,
                RobotAction.MoveSouthWest,
                RobotAction.FastMoveNorth,
                RobotAction.FastMoveEast,
                RobotAction.FastMoveSouth,
                RobotAction.FastMoveWest,
            ]
            for index, (mx, my) in enumerate(zip(MoveDx, MoveDy)):
                if ax == mx and ay == my:
                    return actions[index]
