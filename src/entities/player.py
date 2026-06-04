from typing import Tuple
from src.engine.direction import Direction
from src.entities.controls import Controls


class Player(Controls):
    """Represents the control Pac-Man entity, tracking lives, states, and modifications."""
    def __init__(self, start: Tuple[int, int], live: int, t_size: int) -> None:
        """Initialize player-specific metrics, coordinates, life pool, and tracking states."""
        super().__init__(start, t_size)
        self.live = live
        self.cheat = False
        self.super = False
        self.super_pcgum = 0
        self.pcgum = 0

    def direction(self, direction: Direction) -> None:
        """Buffer the next requested movement direction and force heading updates if stagnant."""
        self.next_direction = direction
        if self.current_direction == Direction.NONE:
            self.current_direction = direction

    def upgrade_lives(self) -> None:
        """Increment the remaining player life counter by one unit."""
        self.live += 1

    def respawn_player(self) -> None:
        """Reset logical grid coordinates and spatial pixel parameters to the spawn point."""
        self.current_zone = self.respawn
        self.pixel_x = self.respawn[0] * self.tile_size
        self.pixel_y = self.respawn[1] * self.tile_size

    def cheat_mode(self) -> None:
        """Toggle the runtime validation status of the evaluation cheat sub-mode flags."""
        self.cheat = not self.cheat

    def update_super_t(self) -> None:
        """Activate the enhanced super-pacgum status condition modifier state."""
        self.super = True

    def update_super_f(self) -> None:
        """Deactivate the enhanced super-pacgum status condition modifier state."""
        self.super = False
