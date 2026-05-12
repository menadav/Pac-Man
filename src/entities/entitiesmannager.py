from typing import List, Tuple
from mazegenerator.mazegenerator import MazeGenerator
from src.parse.models import ParseConfig
from src.entities.items import Items
from src.entities.player import Player
from src.engine.controls import Direction

class EntitiesMannager:
    def __init__(self, data: ParseConfig) -> None:
        self.data = data
        self.level_index = 0
        self.current_level = self.data.levels[self.level_index]
        self.maze_engine = MazeGenerator(
            size=(self.current_level.width, self.current_level.height),
            seed=42,
            perfect=False
        )
        self.items = Items(self.current_level.pacgum, self.maze_engine.maze)
        self.matrix = self.items.apply_to_matrix()
        self.player = Player(self.items.respawn)
        self.status = "RUNNING"

    def next_level(self) -> None:
        self.level_index += 1
        self.current_level = self.data.levels[self.level_index]
        self.maze_engine = MazeGenerator(
            size=(self.current_level.width, self.current_level.height),
            perfect=False
        )
        self.items = Items(self.current_level.pacgum, self.maze_engine.maze)
        self.matrix = self.items.apply_to_matrix()
        self.player = Player(self.items.start())

    def can_move(
            self,
            current: Tuple[int , int],
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
        current_pos = self.player.current_zone
        if self.can_move(current_pos, self.player.next_direction):
            self.player.current_direction = self.player.next_direction
        if self.can_move(current_pos, self.player.current_direction):
            self.player.update_zone()
        else:
            self.player.current_direction = Direction.NONE