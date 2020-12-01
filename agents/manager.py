from typing import Callable, Iterable

from agents.baby_agent import BabyAgent
from agents.robot_agent import RobotAgent
from agents.room_environment import RoomEnvironment
from agents.statistics_model import StatisticsModel


class Manager:
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

    def run(self, n_test: int = 30) -> Iterable[StatisticsModel]:
        victory = 0
        defeat = 0
        tie = 0
        dirt = 0
        for _ in range(n_test):
            room = RoomEnvironment(
                self.n_rows,
                self.n_columns,
                self.n_robots,
                self.n_babies,
                self.n_obstacles,
                self.n_dirts,
                self.random_time,
                self.dirt_probability,
                self.robot_creator,
                self.baby_creator,
            )
            while True:
                total_free_cells = room.n_dirts + room.free
                if (room.n_dirts / total_free_cells) * 100 >= 40:
                    defeat += 1
                    dirt += room.n_dirts
                    break
                if room.is_clean():
                    victory += 1
                    dirt += room.n_dirts
                    break
                if room.time == room.random_time * 100:
                    tie += 1
                    dirt += room.n_dirts
                    break
                room.next_step()
            yield StatisticsModel(victory, defeat, tie, dirt / n_test)
