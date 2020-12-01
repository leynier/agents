from typing import Optional

import typer

from agents.baby_agent import BabyAgent
from agents.manager import Manager
from agents.model_reflex_robot_agent import ModelReflexRobotAgent
from agents.random_robot_agent import RandomRobotAgent
from agents.statistics_model import StatisticsModel

app = typer.Typer()


@app.command()
def model_reflex(n: int = 30):
    n_rows = [5, 7, 10, 12, 14, 16, 18, 20, 22, 25]
    n_columns = [5, 7, 10, 12, 14, 16, 18, 20, 22, 25]
    n_babies = [2, 3, 4, 5, 3, 4, 5, 3, 4, 5]
    n_obstacles = [5, 15, 20, 25, 15, 20, 25, 15, 20, 25]
    n_dirts = [5, 10, 20, 30, 10, 20, 30, 10, 20, 30]
    random_time = [10, 10, 10, 15, 15, 15, 20, 20, 20, 25]
    for i, _ in enumerate(n_rows):
        manager = Manager(
            n_rows=n_rows[i],
            n_columns=n_columns[i],
            n_robots=1,
            n_babies=n_babies[i],
            n_obstacles=n_obstacles[i],
            n_dirts=n_dirts[i],
            random_time=random_time[i],
            dirt_probability=0.3,
            robot_creator=lambda x, y: ModelReflexRobotAgent(x, y),
            baby_creator=lambda x, y: BabyAgent(x, y),
        )
        last_model: Optional[StatisticsModel] = None
        for model in manager.run(n):
            last_model = model
        result = f"{last_model.victory}, {last_model.tie}, "
        result += f"{last_model.defeat}, {last_model.dirt}"
        typer.echo(result)


@app.command()
def random(n: int = 30):
    n_rows = [5, 7, 10, 12, 14, 16, 18, 20, 22, 25]
    n_columns = [5, 7, 10, 12, 14, 16, 18, 20, 22, 25]
    n_babies = [2, 3, 4, 5, 3, 4, 5, 3, 4, 5]
    n_obstacles = [5, 15, 20, 25, 15, 20, 25, 15, 20, 25]
    n_dirts = [5, 10, 20, 30, 10, 20, 30, 10, 20, 30]
    random_time = [10, 10, 10, 15, 15, 15, 20, 20, 20, 25]
    for i, _ in enumerate(n_rows):
        manager = Manager(
            n_rows=n_rows[i],
            n_columns=n_columns[i],
            n_robots=1,
            n_babies=n_babies[i],
            n_obstacles=n_obstacles[i],
            n_dirts=n_dirts[i],
            random_time=random_time[i],
            dirt_probability=0.3,
            robot_creator=lambda x, y: RandomRobotAgent(x, y),
            baby_creator=lambda x, y: BabyAgent(x, y),
        )
        last_model: Optional[StatisticsModel] = None
        for model in manager.run(n):
            last_model = model
        result = f"{last_model.victory}, {last_model.tie}, "
        result += f"{last_model.defeat}, {last_model.dirt}"
        typer.echo(result)
