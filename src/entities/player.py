from typing import Tuple
from src.engine.direction import Direction
from src.entities.entitie import Controls


class Player(Controls):
    def __init__(self, start: Tuple[int, int], live: int, t_size: int) -> None:
        super().__init__(start, t_size)
        self.live = live
        self.cheat = False
        self.super = False
        self.super_pcgum = 0
        self.pcgum = 0

    def direction(self, direction: Direction) -> None:
        self.next_direction = direction
        if self.current_direction == Direction.NONE:
            self.current_direction = direction

    def upgrade_lives(self) -> None:
        self.live += 1

    def respawn_player(self) -> None:
        self.current_zone = self.respawn
        self.pixel_x = self.respawn[0] * self.tile_size
        self.pixel_y = self.respawn[1] * self.tile_size

    def cheat_mode(self) -> None:
        self.cheat = not self.cheat

    def update_super_t(self) -> None:
        self.super = True

    def update_super_f(self) -> None:
        self.super = False
