import Abstractmethod
from abc import ABC, abstractmethod
from src.engine.controls import Direction


class Ghost(ABC):
    def __init__(
            self,
            start: Tuple[int, int],
            scatter_target: Tuple[int, int]
            ) -> None:
        self.current_zone = start
        self.spawn_point = start
        self.scatter_target = scatter_target
        self.current_direction = Direction.NONE
        self.next_direction = Direction.NONE


    @abstractmethod
    def calculate_target(
            self,
            player_zone: Tuple[int, int],
            player_dir: Direction
            ) -> Tuple[int, int]:
        pass

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
