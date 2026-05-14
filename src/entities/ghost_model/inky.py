from typing import Tuple
from src.engine.direction import Direction
from src.entities.ghost_model.ghost import Ghost


class Inky(Ghost):
    def __init__(self, start: Tuple[int, int], scatter_target, tile_size) -> None:
        super().__init__(start, scatter_target, tile_size)

    def calculate_target(
            self,
            player_zone: Tuple[int, int],
            player_dir: Direction
            ) -> Tuple[int, int]:
        return player_zone
