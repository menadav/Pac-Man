from typing import Tuple

from src.engine.direction import Direction
from src.entities.ghost_model.ghost import Ghost


class Pinky(Ghost):
    """Pinky ghost implementation that ambush-targets the player by looking ahead."""
    def __init__(
        self,
        start: Tuple[int, int],
        scatter_target: Tuple[int, int],
        tile_size: int,
    ) -> None:
        """Initialize Pinky with starting coordinates, scatter destinations, and sizing."""
        super().__init__(start, scatter_target, tile_size)

    def calculate_target(
        self, player_zone: Tuple[int, int], player_dir: Direction
    ) -> Tuple[int, int]:
        """Project an ambush target coordinate exactly 4 tiles ahead of the player's vector."""
        move_map = {
            Direction.UP: (0, -4),
            Direction.DOWN: (0, 4),
            Direction.LEFT: (-4, 0),
            Direction.RIGHT: (4, 0),
            Direction.NONE: (0, 0),
        }
        dx, dy = move_map[player_dir]
        return player_zone[0] + dx, player_zone[1] + dy
