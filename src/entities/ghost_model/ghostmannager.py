from src.entities.items import Items
from src.entities.ghost_model.blinky import Blinky
from src.entities.ghost_model.pinky import Pinky
from src.entities.ghost_model.inky import Inky
from src.entities.ghost_model.clyde import Clyde

class GhostMannager:
    def __init__(self, item: Items, t_size: int) -> None:
        self.items = item
        w = self.items._width
        h = self.items._height
        self.pinky = Pinky((1, 0), (0,0), t_size) 
        self.blinky = Blinky((w - 2, 0), (w - 1, 0), t_size)
        self.clyde = Clyde((1, h - 2), (0, h - 1), t_size)
        self.inky = Inky((w - 2, h - 1) ,(w - 1, h - 1), t_size)
        
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

    def update(self, player_zone, player_dir, can_move_func, matrix):
        for ghost in self.ghosts:
            ghost.update_ghost(player_zone, player_dir, can_move_func, matrix)
