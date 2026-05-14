from typing import Tuple
from src.engine.direction import Direction


class Controls:
    def __init__(self, start: Tuple[int, int], tile_size: int) -> None:
        self.current_zone = start
        self.respawn = start
        self.current_direction = Direction.NONE
        self.next_direction = Direction.NONE
        self.tile_size = tile_size
        self.pixel_x = float(start[0] * self.tile_size)
        self.pixel_y = float(start[1] * self.tile_size)
        self.speed = 2.0

    def is_centered(self) -> bool:
        return self.pixel_x % self.tile_size == 0 and self.pixel_y % self.tile_size == 0

    def update_position(self) -> None:
        # Movimiento normal
        if self.current_direction == Direction.UP:
            self.pixel_y -= self.speed
        elif self.current_direction == Direction.DOWN:
            self.pixel_y += self.speed
        elif self.current_direction == Direction.LEFT:
            self.pixel_x -= self.speed
        elif self.current_direction == Direction.RIGHT:
            self.pixel_x += self.speed
        if self.current_direction in [Direction.LEFT, Direction.RIGHT]:
            self.pixel_y = float(round(self.pixel_y / self.tile_size) * self.tile_size)
        elif self.current_direction in [Direction.UP, Direction.DOWN]:
            self.pixel_x = float(round(self.pixel_x / self.tile_size) * self.tile_size)

        self._check_zone_boundary()

    def _check_zone_boundary(self) -> None:
        self.current_zone = (
            int(round(self.pixel_x) // self.tile_size),
            int(round(self.pixel_y) // self.tile_size)
        )
