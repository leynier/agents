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
    manager = Manager(
        15,
        15,
        3,
        5,
        5,
        5,
        100,
        0.4,
        lambda x, y: ModelReflexRobotAgent(x, y),
        lambda x, y: BabyAgent(x, y),
    )
    last_model: Optional[StatisticsModel] = None
    with typer.progressbar(manager.run(n), length=n) as models:
        for model in models:
            last_model = model
    typer.echo(last_model)


@app.command()
def random(n: int = 30):
    manager = Manager(
        5,
        15,
        3,
        5,
        5,
        5,
        100,
        0.4,
        lambda x, y: RandomRobotAgent(x, y),
        lambda x, y: BabyAgent(x, y),
    )
    last_model: Optional[StatisticsModel] = None
    with typer.progressbar(manager.run(n), length=n) as models:
        for model in models:
            last_model = model
    typer.echo(last_model)
