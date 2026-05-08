from mazegenerator.mazegenerator import MazeGenerator
from src.parse.models import ParseConfig


class EntitiesMannager:
    def __init__(self, data: ParseConfig) -> None:
        print("DEBUG 1: Entrando en EntitiesMannager")
        self.data = data
        self.level_index = 0
        self.current_level = self.data.levels[self.level_index]
        print(f"DEBUG 2: Generando laberinto {self.current_level.width}x{self.current_level.height}...")
        self.maze_engine = MazeGenerator(
            size=(self.current_level.width, self.current_level.height),
            perfect=True # Ponlo en True para asegurar que no se buclee
        )
        print("DEBUG 3: ¡Laberinto generado con éxito!")
        self.matrix = self.maze_engine.maze
        self.status = "RUNNING"