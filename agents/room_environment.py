from random import randint, random
from typing import Any, Callable, List, Tuple, cast

from agents.baby_action import BabyAction
from agents.baby_agent import BabyAgent
from agents.cell import Cell
from agents.directions import Dx, Dy
from agents.robot_action import RobotAction
from agents.robot_agent import RobotAgent, RobotDx, RobotDy
from agents.thing import Thing
from agents.visitor import on, when


class RoomEnvironment:
    def __init__(
        self,
        n_rows: int,
        n_columns: int,
        n_robots: int,
        n_babies: int,
        n_obstacles: int,
        n_dirts: int,
        random_time: int,
        dirt_probability: float,
        robot_creator: Callable[[int, int], RobotAgent],
        baby_creator: Callable[[int, int], BabyAgent],
    ):
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.n_robots = n_robots
        self.n_babies = n_babies
        self.n_obstacles = n_obstacles
        self.n_dirts = n_dirts
        self.random_time = random_time
        self.dirt_probability = dirt_probability
        self.robot_creator = robot_creator
        self.baby_creator = baby_creator

        self.matrix = [[Cell.Free for _ in range(n_columns)] for _ in range(n_rows)]
        self.robots: List[RobotAgent] = []
        self.babies: List[BabyAgent] = []
        self.time = 0
        self.free = n_rows * n_columns - n_obstacles - n_dirts - n_babies

        # Config agents and environment
        (x, y), *_ = self.config_environment(Cell.Barnyard, 1)
        self.config_barnyard(x, y, n_babies - 1)
        self.config_environment(Cell.Obstacle, n_obstacles)
        self.config_environment(Cell.Dirty, n_dirts)
        self.config_agents(robot_creator, self.robots, n_robots)
        self.config_agents(baby_creator, self.babies, n_babies)

    def next_step(self):
        for robot in self.robots:
            self.execute_action(robot, robot.get_action(self))
        for baby in self.babies:
            self.execute_action(baby, baby.get_action(self))
        if not self.time % self.random_time:
            self.randomize()
        self.time += 1

    @on("agent")
    def execute_action(self, agent, action):
        pass

    @when(RobotAgent)
    def execute_action(self, robot: RobotAgent, action: RobotAction):  # noqa:F811
        mx = RobotDx[action.value - 1]
        my = RobotDy[action.value - 1]
        if action == RobotAction.Hold:
            return
        elif action == RobotAction.Clean:
            if self.matrix[robot.x][robot.y] == Cell.Dirty:
                self.matrix[robot.x][robot.y] = Cell.Free
                self.n_dirts -= 1
                self.free += 1
                return
        elif action == RobotAction.DropBaby:
            if self.matrix[robot.x][robot.y] != Cell.Dirty:
                if robot.baby is not None:
                    cast(BabyAgent, robot.baby).robot = None
                robot.baby = None
            return
        elif (
            self.is_valid(robot.x + mx, robot.y + my)
            and self.matrix[robot.x + mx][robot.y + my] != Cell.Obstacle
            and not any(
                [
                    other.x == robot.x + mx and other.y == robot.y + my
                    for other in self.robots
                ]
            )
        ):
            if not self.is_occupied(robot.x + mx, robot.y + my):
                robot.x += mx
                robot.y += my
                if robot.is_loading():
                    robot.baby.x += mx
                    robot.baby.y += my
            elif not robot.is_loading():
                babies = [
                    baby
                    for baby in self.babies
                    if baby.x == robot.x + mx and baby.y == robot.y + my
                ]
                assert babies
                baby = babies[0]
                robot.baby = baby
                baby.robot = robot
                robot.x += mx
                robot.y += my

    @when(BabyAgent)
    def execute_action(self, baby: BabyAgent, action: BabyAction):  # noqa:F811
        if action == BabyAction.Hold or baby.is_loaded():
            return
        mx, my = Dx[action.value - 1], Dy[action.value - 1]
        if self.baby_push(baby.x + mx, baby.y + my, mx, my):
            tmx = baby.x
            tmy = baby.y
            baby.x = tmx + mx
            baby.y = tmy + my
            self.baby_dirt(tmx, tmy)

    def baby_dirt(self, x, y):
        if random() > self.dirt_probability:
            return
        babies_around = [
            baby for baby in self.babies if abs(x - baby.x) < 2 and abs(y - baby.y) < 2
        ]
        to_dirt = 9 - len(babies_around)
        if len(babies_around) == 1:
            to_dirt = 1
        if len(babies_around) == 2:
            to_dirt = 3
        cedx = list(Dx + [0, 1, -1, -1, 1])
        cedy = list(Dy + [0, 1, -1, 1, -1])
        while to_dirt and cedx:
            pos = randint(0, min(3, len(cedx) - 1))
            mx, my = cedx.pop(pos), cedy.pop(pos)
            if self.is_free(x + mx, y + my) and not self.is_occupied(x + mx, y + my):
                self.matrix[x][y] = Cell.Dirty
                self.n_dirts += 1
                self.free -= 1
                to_dirt -= 1

    def baby_push(self, x: int, y: int, mx: int, my: int) -> bool:
        if not self.is_valid(x, y):
            return False
        if self.matrix[x][y] == Cell.Free and not self.is_occupied(x, y):
            return True
        elif self.matrix[x][y] == Cell.Obstacle:
            if self.baby_push(x + mx, y + my, mx, my):
                self.matrix[x][y] = Cell.Free
                self.matrix[x + mx][y + my] = Cell.Obstacle
                return True
        return False

    def randomize(self):
        old_matrix = self.matrix
        self.matrix = [
            [Cell.Free for _ in range(self.n_columns)] for _ in range(self.n_rows)
        ]
        (x, y), *_ = self.config_environment(Cell.Barnyard, 1)
        self.config_barnyard(x, y, self.n_babies - 1)
        self.config_environment(Cell.Obstacle, self.n_obstacles)
        self.config_environment(Cell.Dirty, self.n_dirts)

        for baby in self.babies:
            if old_matrix[baby.x][baby.y] == Cell.Barnyard:
                for row in range(len(self.matrix)):
                    for col in range(len(self.matrix[row])):
                        if self.matrix[row][
                            col
                        ] == Cell.Barnyard and not self.is_occupied(row, col):
                            baby.x = row
                            baby.y = col
            else:
                while True:
                    x, y = (randint(0, self.n_rows - 1), randint(0, self.n_columns - 1))
                    if self.matrix[x][y] != Cell.Free or self.is_occupied(x, y):
                        continue
                    baby.x = x
                    baby.y = y
                    break

        for robot in self.robots:
            while True:
                x, y = (randint(0, self.n_rows - 1), randint(0, self.n_columns - 1))
                if self.matrix[x][y] != Cell.Free or self.is_occupied(x, y):
                    continue
                robot.x = x
                robot.y = y
                if robot.is_loading():
                    robot.baby.x = x
                    robot.baby.y = y
                break

    def config_environment(
        self,
        cell: Cell,
        count: int,
    ) -> List[Tuple[int, int]]:
        result: List[Tuple[int, int]] = []
        for _ in range(count):
            while True:
                x, y = (randint(0, self.n_rows - 1), randint(0, self.n_columns - 1))
                if self.matrix[x][y] != Cell.Free:
                    continue
                self.matrix[x][y] = cell
                result.append((x, y))
                break
        return result

    def config_barnyard(self, x: int, y: int, count: int):
        queue = [(x, y)]
        while queue:
            row, column = queue.pop(0)
            for dx, dy in zip(Dx, Dy):
                if count <= 0:
                    return
                row = row + dx
                column = column + dy
                if self.is_free(row, column):
                    self.matrix[row][column] = Cell.Barnyard
                    queue.append((row, column))
                    count -= 1

    def config_agents(
        self,
        model_agent: Callable[[int, int], Any],
        agents: List[Any],
        count: int,
    ):
        for _ in range(count):
            while True:
                x, y = (randint(0, self.n_rows - 1), randint(0, self.n_columns - 1))
                if self.is_occupied(x, y) or not self.is_free(x, y):
                    continue
                agents.append(model_agent(x, y))
                break

    def is_valid(self, x, y):
        return 0 <= x < self.n_rows and 0 <= y < self.n_columns

    def is_free(self, x, y):
        return self.is_valid(x, y) and self.matrix[x][y] == Cell.Free

    def is_occupied(self, x, y):
        return any(
            item.x == x and item.y == y
            for item in cast(List[Thing], self.robots) + cast(List[Thing], self.babies)
        )

    def is_clean(self) -> bool:
        for row in self.matrix:
            for cell in row:
                if cell == Cell.Dirty:
                    return False
        return all(self.matrix[baby.x][baby.y] == Cell.Barnyard for baby in self.babies)

    def __str__(self):
        result = ""
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                cell = ""
                if self.matrix[i][j] == Cell.Free:
                    cell = ". "
                if self.matrix[i][j] == Cell.Barnyard:
                    cell = "C "
                if self.matrix[i][j] == Cell.Dirty:
                    cell = "D "
                if self.matrix[i][j] == Cell.Obstacle:
                    cell = "X "
                if any([robot.x == i and robot.y == j for robot in self.robots]):
                    cell = "R "
                if any([baby.x == i and baby.y == j for baby in self.babies]):
                    cell = "B "
                result += cell
            result += "\n"
        # result += legend
        return result
