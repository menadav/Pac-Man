from typing import Tuple
from mazegenerator.mazegenerator import MazeGenerator
from src.parse.models import ParseConfig
from src.entities.items import Items
from src.entities.player import Player
from src.engine.direction import Direction


class EntitiesMannager:
    def __init__(self, data: ParseConfig) -> None:
        self.data = data
        self.level_index = 0
        self.bit_superpcgum = 32
        self.bit_pcgum = 16
        self.current_level = self.data.levels[self.level_index]
        self.maze_engine = MazeGenerator(
            size=(self.current_level.width, self.current_level.height),
            seed=42,
            perfect=False
        )
        self.items = Items(self.current_level.pacgum, self.maze_engine.maze)
        self.matrix = self.items.apply_to_matrix()
        self.actual_live = self.data.lives
        self.player = Player(self.items.respawn, self.actual_live)
        self.lvl_items = self.current_level.pacgum + 4
        self.score = 0
        self.status = "RUNNING"

    def next_level(self) -> None:
        self.level_index += 1
        if self.level_index == len(self.data.levels):
            self.status = "WIN"
            return
        self.current_level = self.data.levels[self.level_index]
        self.lvl_items = self.current_level.pacgum + 4
        self.maze_engine = MazeGenerator(
            size=(self.current_level.width, self.current_level.height),
            perfect=False
        )
        self.items = Items(self.current_level.pacgum, self.maze_engine.maze)
        self.matrix = self.items.apply_to_matrix()
        self.player = Player(self.items.respawn, self.actual_live)

    def can_move(
            self,
            current: Tuple[int, int],
            move: Direction
            ) -> bool:
        if move == Direction.NONE:
            return False
        x, y = current
        cell_vallue = self.matrix[y][x]
        masks = {
            Direction.UP: 1,
            Direction.RIGHT: 2,
            Direction.DOWN: 4,
            Direction.LEFT: 8
        }
        return (cell_vallue & masks[move]) == 0

    def update(self) -> None:
        if self._check_live(self.player.live):
            self.status = "END"
        current_pos = self.player.current_zone
        if self.can_move(current_pos, self.player.next_direction):
            self.player.current_direction = self.player.next_direction
        if self.can_move(current_pos, self.player.current_direction):
            self.player.update_zone()
            pos = self.player.current_zone
            if self._check_bit(pos, self.bit_superpcgum):
                self._update_bit_score(pos, self.bit_superpcgum)
            elif self._check_bit(pos, self.bit_pcgum):
                self._update_bit_score(pos, self.bit_pcgum)
            if self._check_lvl():
                self.next_level()
        else:
            self.player.current_direction = Direction.NONE
    
    def _check_lvl(self) -> bool:
        total_pcgum = self.player.super_pcgum + self.player.pcgum
        if self.lvl_items == total_pcgum:
            return True
        return False

    def _check_live(self, live: int) -> None:
        if live < 0:
            self.game_mannager.status = "END"

    def _check_bit(
            self,
            pos: Tuple[int, int],
            bit: int
            ) -> bool:
        x, y = pos
        return (self.matrix[y][x] & bit) != 0

    def _update_bit_score(self, pos: Tuple[int, int], bit: int) -> None:
        x, y = pos
        self.matrix[y][x] &= ~bit
        if bit == self.bit_pcgum:
            self.player.pcgum += 1
            self._update_pcgum()
        elif bit == self.bit_superpcgum:
            self.player.super_pcgum += 1
            self._update_superpcgum()

    def _update_pcgum(self) -> None:
        self.score += self.data.points_per_pacgum

    def _update_superpcgum(self) -> None:
        self.score += self.data.points_per_super_pacgum
