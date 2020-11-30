from typing import Optional

from agents.agent import Agent

RobotDx = [-1, 0, 1, 0, 0, 0, 0, 1, -1, -1, 1, -2, 0, 2, 0]
RobotDy = [0, 1, 0, -1, 0, 0, 0, 1, -1, 1, -1, 0, 2, 0, -2]


class RobotAgent(Agent):
    def __init__(self, x, y):
        super(RobotAgent, self).__init__(x, y)
        self.baby: Optional[Agent] = None

    def is_loading(self) -> bool:
        return self.baby is not None
