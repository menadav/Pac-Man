from typing import Tuple
from abc import ABC, abstractmethod
from src.engine.direction import Direction
from src.entities.entitie import Controls


class Ghost(Controls, ABC):
    def __init__(
            self,
            start: Tuple[int, int],
            scatter_target: Tuple[int, int],
            tile_size: int
            ) -> None:
        super().__init__(start, tile_size)
        self.scatter_target = scatter_target
        self.mode = "CHASE"
        self.speed = 1

    @abstractmethod
    def calculate_target(
            self,
            player_zone: Tuple[int, int],
            player_dir: Direction
            ) -> Tuple[int, int]:
        pass

    def update_ghost(self, player_zone, player_dir, can_move_func):
        if self.mode == "CHASE":
            target = self.calculate_target(player_zone, player_dir)
        else:
            target = self.scatter_target
        if (self.pixel_x % self.tile_size == 0 and self.pixel_y % self.tile_size == 0) \
                or self.current_direction == Direction.NONE:
            new_dir = self._ai_decide_direction(target, can_move_func)
            if self.current_direction == Direction.NONE and not can_move_func(self.current_zone, new_dir):
                self.current_direction = Direction.NONE
            else:
                self.current_direction = new_dir
        self.update_position()

    def _ai_decide_direction(
            self, target: Tuple[int, int],
            can_move_func
            ) -> Direction:
        directions = [
            Direction.UP, Direction.DOWN,
            Direction.LEFT, Direction.RIGHT
            ]
        move_map = {
            Direction.UP: (0, -1), Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0), Direction.RIGHT: (1, 0)
        }
        opposite = {
            Direction.UP: Direction.DOWN, Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT, Direction.RIGHT: Direction.LEFT,
            Direction.NONE: Direction.NONE
        }
        possibl_direction = [d for d in directions if can_move_func(self.current_zone, d)]
        if not possibl_direction:
            return Direction.NONE
        if self.current_direction == Direction.NONE:
            forward_directions = possibl_direction
        else:
            forward_directions = [
                d for d in possibl_direction
                if d != opposite[self.current_direction]
            ]
        best_direction = forward_directions[0] if forward_directions else possibl_direction[0]
        min_distance = float('inf')
        if forward_directions:
            for d in forward_directions:
                dx, dy = move_map[d]
                next_x, next_y = (
                    self.current_zone[0] + dx, self.current_zone[1] + dy
                )
                dist = ((target[0] - next_x)**2 + (target[1] - next_y)**2)**0.5
                if dist < min_distance:
                    min_distance = dist
                    best_direction = d
        else:
            best_direction = opposite[self.current_direction]
        return best_direction
