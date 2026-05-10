from typing import Tuple

class Player:
    def __init__(self, start: Tuple(int, int)) -> None:
        self.current_zone = start
        self.super_pcgum = 0
        self.pcgum = 0

    def update_zone(self) -> None:
        pass
