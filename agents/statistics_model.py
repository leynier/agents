class StatisticsModel:
    def __init__(self, victory: int, defeat: int, tie: int, dirt: float):
        self.victory = victory
        self.defeat = defeat
        self.tie = tie
        self.dirt = dirt

    def __str__(self) -> str:
        result = f"Robot's victories: {self.victory}\n"
        result += f"Robot's defeats: {self.defeat}\n"
        result += f"Simulations with end inconclusive: {self.tie}\n"
        result += f"The average amount of dirty cells: {self.dirt}"
        return result
