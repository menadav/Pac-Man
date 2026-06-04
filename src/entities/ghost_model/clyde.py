from typing import Tuple

from src.engine.direction import Direction
from src.entities.ghost_model.ghost import Ghost


class Clyde(Ghost):
    """Clyde ghost implementation that changes proximity routing based on player distance."""
    def __init__(
        self,
        start: Tuple[int, int],
        scatter_target: Tuple[int, int],
        t_size: int,
    ) -> None:
        """Initialize Clyde with starting coordinates, scatter destinations, and sizing."""
        super().__init__(start, scatter_target, t_size)

    def calculate_target(
        self, player_zone: Tuple[int, int], player_dir: Direction
    ) -> Tuple[int, int]:
        """Target the player when far away, or default to the scatter corner when close."""
        dist = (
            (self.current_zone[0] - player_zone[0]) ** 2
            + (self.current_zone[1] - player_zone[1]) ** 2
        ) ** 0.5
        if dist > 8:
            return player_zone
        else:
            return self.scatter_target
