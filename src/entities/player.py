from typing import Tuple
from src.engine.controls import Direction


class Player:
    def __init__(self, start: Tuple[int, int], live: int) -> None:
        self.current_zone = start
        self.current_direction = Direction.NONE
        self.next_direction = Direction.NONE
        self.live = live
        self.cheat_mode = False
        self.super_pcgum = 0
        self.pcgum = 0

    def direction(self, direction: Direction) -> None:
        self.next_direction = direction

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

    def upgrade_lives(self) -> None:
        self.live += 1

    def cheat_mode(self) -> None:
        self.cheat_mode = not self.cheat_mode
