from typing import Tuple
from abc import ABC, abstractmethod
from src.engine.direction import Direction
from src.entities.entitie import Controls


class Ghost(Controls, ABC):
    def __init__(
            self,
            start: Tuple[int, int],
            scatter_target: Tuple[int, int]
            ) -> None:
        super().__init__(start)
        self.scatter_target = scatter_target

    @abstractmethod
    def calculate_target(
            self,
            player_zone: Tuple[int, int],
            player_dir: Direction
            ) -> Tuple[int, int]:
        pass
