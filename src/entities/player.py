from typing import Tuple

class Player:
    def __init__(self, start: Tuple[int, int]) -> None:
        self.current_zone = start
        self.move = "LEFT"
        self.super_pcgum = 0
        self.pcgum = 0

    def direction(self, direction: str) -> None:
        self.move = direction


    def update_zone(self, new_zone: Tuple[int, int]) -> None:
        x, y = self.current_zone
        nx, ny = new_zone
        self.current_zone = x + nx, y + ny
