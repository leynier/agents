from agents.action import Action
from agents.thing import Thing


class Agent(Thing):
    def __init__(self, x: int, y: int):
        super(Agent, self).__init__(x, y)

    def get_action(self, environment) -> Action:
        raise NotImplementedError()
