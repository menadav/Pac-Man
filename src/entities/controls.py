from typing import Tuple
from src.engine.direction import Direction


class Controls:
    """Handles positioning, directional steering, and alignment logic for a moving entity."""
    def __init__(self, start: Tuple[int, int], tile_size: int) -> None:
        """Initialize the layout state, starting vectors, speed, and geometric pixel mappings."""
        self.current_zone = start
        self.respawn = start
        self.current_direction = Direction.NONE
        self.next_direction = Direction.NONE
        self.tile_size = tile_size
        self.pixel_x = float(start[0] * self.tile_size)
        self.pixel_y = float(start[1] * self.tile_size)
        self.speed = 3

    def is_centered(self) -> bool:
        """Determine if the entity is perfectly snapped to the center axis of a single tile."""
        return (
            self.pixel_x % self.tile_size == 0
            and self.pixel_y % self.tile_size == 0
        )

    def update_position(self) -> None:
        """Increment pixel coordinates along the heading vector and snap opposite axes to bounds."""
        if self.current_direction == Direction.UP:
            self.pixel_y -= self.speed
        elif self.current_direction == Direction.DOWN:
            self.pixel_y += self.speed
        elif self.current_direction == Direction.LEFT:
            self.pixel_x -= self.speed
        elif self.current_direction == Direction.RIGHT:
            self.pixel_x += self.speed
        if self.current_direction in [Direction.LEFT, Direction.RIGHT]:
            self.pixel_y = float(
                round(self.pixel_y / self.tile_size) * self.tile_size)
        elif self.current_direction in [Direction.UP, Direction.DOWN]:
            self.pixel_x = float(
                round(self.pixel_x / self.tile_size) * self.tile_size)
        self._check_zone_boundary()

    def _check_zone_boundary(self) -> None:
        """Recalculate the discrete logical grid coordinates based on current continuous pixel."""
        self.current_zone = (
            int(round(self.pixel_x) // self.tile_size),
            int(round(self.pixel_y) // self.tile_size)
        )
