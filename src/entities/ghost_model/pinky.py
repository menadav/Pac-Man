from typing import Tuple
from src.engine.direction import Direction
from src.entities.ghost_model.ghost import Ghost


class Pinky(Ghost):
    def __init__(self, start: Tuple[int, int]) -> None:
        super().__init__(start, scatter_target(25, 0))

    def calculate_target(
            self,
            player_zone: Tuple[int, int],
            player_dir: Direction
            ) -> Tuple[int, int]:
        pass
