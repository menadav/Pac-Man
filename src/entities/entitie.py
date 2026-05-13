from typing import Tuple
from src.engine.direction import Direction


class Controls:
    def __init__(self, start: Tuple[int, int]) -> None:
        self.current_zone = start
        self.respawn = start
        self.current_direction = Direction.NONE
        self.next_direction = Direction.NONE

    def update_zone(self) -> None:
        x, y = self.current_zone
        if self.current_direction == Direction.UP:
            self.current_zone = (x, y - 1)
        elif self.current_direction == Direction.DOWN:
            self.current_zone = (x, y + 1)
        elif self.current_direction == Direction.LEFT:
            self.current_zone = (x - 1, y)
        elif self.current_direction == Direction.RIGHT:
            self.current_zone = (x + 1, y)
