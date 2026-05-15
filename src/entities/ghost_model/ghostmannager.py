from typing import List, Tuple
from src.engine.direction import Direction
from src.entities.items import Items
from src.entities.ghost_model.blinky import Blinky
from src.entities.ghost_model.pinky import Pinky
from src.entities.ghost_model.inky import Inky
from src.entities.ghost_model.clyde import Clyde


class GhostMannager:
    def __init__(self, item: Items, t_size: int) -> None:
        self.items = item
        self.w = self.items._width
        self.h = self.items._height
        self.pinky = Pinky((1, 0), (0, 0), t_size) 
        self.blinky = Blinky((self.w - 2, 0), (self.w - 1, 0), t_size)
        self.clyde = Clyde((1, self.h - 2), (0, self.h - 1), t_size)
        self.inky = Inky(
            (self.w - 2, self.h - 1), (self.w - 1, self.h - 1), t_size)
        self.time_escape = float('inf')
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

    def update(self, player_zone, player_dir, can_move_func, actual_time):
        for ghost in self.ghosts:
            if self.time_escape < actual_time:
                ghost.mode = "ESCAPE"
            else:
                ghost.mode = "CHASE"
            ghost.update_ghost(player_zone, player_dir, can_move_func)

    def get_ghost_positions(self) -> List[Tuple[int, int]]:
        pos: List[int, int] = []
        for ghost in self.ghosts:
            pos.append(ghost.current_zone)
        return pos
    
    def respawn_ghost(self) -> None:
        initial_positions = {
            self.pinky: (1, 0),
            self.blinky: (self.w - 2, 0),
            self.clyde: (1, self.h - 2),
            self.inky: (self.w - 2, self.h - 1)
        }
        for ghost, start_zone in initial_positions.items():
            ghost.current_zone = start_zone
            ghost.pixel_x = start_zone[0] * ghost.tile_size
            ghost.pixel_y = start_zone[1] * ghost.tile_size
            ghost.current_direction = Direction.NONE
            ghost.mode = "CHASE"
