from typing import List
from mazegenerator.mazegenerator import MazeGenerator
from src.parse.models import ParseConfig
from src.entities.items import Items
from src.entities.player import Player

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

    def update_matrix(self) -> None:
        pass
