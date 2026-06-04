from typing import Tuple

from src.engine.direction import Direction
from src.entities.ghost_model.ghost import Ghost


class Blinky(Ghost):
    """Blinky ghost implementation that aggressively chases the player's position directly."""
    def __init__(
        self,
        start: Tuple[int, int],
        scatter_target: Tuple[int, int],
        tile_size: int,
    ) -> None:
        """Initialize Blinky with starting coordinates, scatter destinations, and sizing."""
        super().__init__(start, scatter_target, tile_size)

    def calculate_target(
        self, player_zone: Tuple[int, int], player_dir: Direction
    ) -> Tuple[int, int]:
        """Target the exact grid coordinates currently occupied by the player."""
        return player_zone
