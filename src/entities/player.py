from typing import Tuple
from src.engine.direction import Direction
from src.entities.entitie import Controls


class Player(Controls):
    def __init__(self, start: Tuple[int, int]) -> None:
        super().__init__(start)
        self.super_pcgum = 0
        self.pcgum = 0

    def direction(self, direction: Direction) -> None:
        self.next_direction = direction
