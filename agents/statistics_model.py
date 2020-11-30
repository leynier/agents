class StatisticsModel:
    def __init__(self, victory: int, defeat: int, tie: int):
        self.victory = victory
        self.defeat = defeat
        self.tie = tie

    def __str__(self) -> str:
        result = f"Robot's victories: {self.victory}\n"
        result += f"Robot's defeats: {self.defeat}\n"
        result += f"Simulations with end inconclusive: {self.tie}"
        return result
