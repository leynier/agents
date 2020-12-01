from typing import List, Tuple

from agents.cell import Cell
from dijkstra.dijkstra import AbstractDijkstraSPF

MoveDx = [-1, 0, 1, 0, 1, -1, -1, 1, -2, 0, 2, 0]
MoveDy = [0, 1, 0, -1, 1, -1, 1, -1, 0, 2, 0, -2]


class Dijkstra(AbstractDijkstraSPF):
    @staticmethod
    def get_adjacent_nodes(
        environment,
        node: Tuple[int, int],
    ) -> List[Tuple[int, int]]:
        x, y = node
        adjacents: List[Tuple[int, int]] = []
        for dx, dy in zip(MoveDx, MoveDy):
            ax = x + dx
            ay = y + dy
            if (
                environment.is_valid(ax, ay)
                and environment.matrix[ax][ay] != Cell.Obstacle
                and not environment.is_occupied(ax, ay)
            ):
                adjacents.append((ax, ay))
        return adjacents

    @staticmethod
    def get_edge_weight(
        environment,
        src: Tuple[int, int],
        dest: Tuple[int, int],
    ):
        moves = list(zip(MoveDx, MoveDy))
        diff = (dest[0] - src[0], dest[1] - src[1])
        if diff in moves:
            return 1
        raise Exception("get_edge_weight")
