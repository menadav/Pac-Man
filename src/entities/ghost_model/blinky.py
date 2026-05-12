from typing import Tuple
from src.entities.ghost_model.ghost import Ghost

class Blinky(Ghost):
    def __init__(self, start: Tuple[int, int]) -> None:
        super().__init__(start, scatter_target(25, 0))

    def calculate_target(
            self, 
            player_zone: Tuple[int, int],
            player_dir: Direction
            ) -> Tuple[int, int]:
        if self.mode == "CHASE":
            return player_zone
        return self.scatter_target
