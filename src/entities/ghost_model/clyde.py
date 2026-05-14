from typing import Tuple
from src.engine.direction import Direction
from src.entities.ghost_model.ghost import Ghost


class Clyde(Ghost):
    def __init__(self, start: Tuple[int, int], scatter_target, t_size) -> None:
        super().__init__(start, scatter_target, t_size)

    def calculate_target(
            self,
            player_zone: Tuple[int, int],
            player_dir: Direction
            ) -> Tuple[int, int]:
        
        return player_zone

