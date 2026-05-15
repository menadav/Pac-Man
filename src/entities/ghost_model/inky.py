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
        if player_dir in [Direction.LEFT, Direction.RIGHT]:
            return (player_zone[0], player_zone[1] + 2)
        else:
            return (player_zone[0] + 2, player_zone[1])
