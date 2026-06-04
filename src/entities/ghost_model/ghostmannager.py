from typing import Callable, Dict, List, Tuple

from src.engine.direction import Direction
from src.entities.ghost_model.blinky import Blinky
from src.entities.ghost_model.clyde import Clyde
from src.entities.ghost_model.ghost import Ghost
from src.entities.ghost_model.inky import Inky
from src.entities.ghost_model.pinky import Pinky
from src.entities.items import Items

EATEN_RESPAWN_TICKS = 200


class GhostMannager:
    """Manages spawning, layout updates, state shifts, and respawn ticks for all ghosts."""
    def __init__(self, item: Items, t_size: int) -> None:
        """Initialize the ghost collection, tracking maps, freeze status flags, and grid corners."""
        self.items = item
        self.w = self.items._width
        self.h = self.items._height
        self.pinky = Pinky((0, 0), (0, 0), t_size)
        self.blinky = Blinky((self.w - 1, 0), (self.w - 1, 0), t_size)
        self.clyde = Clyde((0, self.h - 1), (0, self.h - 1), t_size)
        self.inky = Inky((self.w - 1, self.h - 1), (self.w - 1, self.h - 1), t_size)
        self._corners: Dict[Ghost, Tuple[int, int]] = {
            self.pinky: (0, 0),
            self.blinky: (self.w - 1, 0),
            self.clyde: (0, self.h - 1),
            self.inky: (self.w - 1, self.h - 1),
        }
        self.time_escape: float = float("inf")
        self.ghosts: List[Ghost] = [self.blinky, self.pinky, self.inky, self.clyde]
        self.frozen: bool = False
        for ghost in self.ghosts:
            ghost.eaten_ticks_left = 0  # type: ignore[attr-defined]

    def update(
        self,
        player_zone: Tuple[int, int],
        player_dir: Direction,
        can_move_func: Callable[[Tuple[int, int], Direction], bool],
        actual_time: int,
        ghost: Ghost,
    ) -> None:
        """Process timers and positions for an individual ghost based on its behavior status."""
        if self.frozen:
            return
        if ghost.mode == "EATEN":
            ghost.eaten_ticks_left -= 1  # type: ignore[attr-defined]
            if ghost.eaten_ticks_left <= 0:  # type: ignore[attr-defined]
                self._respawn_to_corner(ghost)
            return
        if self.time_escape > actual_time:
            ghost.mode = "CHASE"
        ghost.update_ghost(player_zone, player_dir, can_move_func)

    def get_active_ghost_positions(self) -> List[Tuple[int, int]]:
        """Retrieve logical grid tracking coordinates for all active, non-eaten ghosts."""
        return [ghost.current_zone for ghost in self.ghosts if ghost.mode != "EATEN"]

    def get_ghost_positions(self) -> List[Tuple[int, int]]:
        """Retrieve logical grid coordinates for active ghosts within the game scene."""
        return self.get_active_ghost_positions()

    def mark_eaten(self, pos: Tuple[int, int]) -> bool:
        """Transition a ghost to the eaten state if it intersects with the targeted position."""
        for ghost in self.ghosts:
            if ghost.mode == "ESCAPE" and ghost.current_zone == pos:
                ghost.mode = "EATEN"
                ghost.eaten_ticks_left = (  # type: ignore[attr-defined]
                    EATEN_RESPAWN_TICKS
                )
                ghost.current_direction = Direction.NONE
                return True
        return False

    def respawn_ghost(self, pos: Tuple[int, int] | None = None) -> None:
        """Reset all ghosts back to spawn maps or flag a single target as eaten."""
        if pos is not None:
            self.mark_eaten(pos)
            return
        for ghost in self.ghosts:
            self._respawn_to_corner(ghost)

    def _respawn_to_corner(self, ghost: Ghost) -> None:
        """Force-snap a specific ghost instance back onto its designated base layout corner."""
        start_zone = self._corners[ghost]
        ghost.current_zone = start_zone
        ghost.pixel_x = start_zone[0] * ghost.tile_size
        ghost.pixel_y = start_zone[1] * ghost.tile_size
        ghost.current_direction = Direction.NONE
        ghost.mode = "CHASE"
        ghost.eaten_ticks_left = 0  # type: ignore[attr-defined]

    def check_status(self, pos: Tuple[int, int]) -> bool:
        """Verify if any vulnerable ghost in escape mode currently occupies a given coordinate."""
        for ghost in self.ghosts:
            if ghost.current_zone == pos and ghost.mode == "ESCAPE":
                return True
        return False

    def ghost_escape(self) -> None:
        """Trigger panic behavior and force vulnerable escape states on all non-eaten ghosts."""
        for ghost in self.ghosts:
            if ghost.mode == "EATEN":
                continue
            ghost.speed = 1
            ghost.mode = "ESCAPE"
            ghost.current_direction = Direction.NONE

    def toggle_freeze(self) -> None:
        """Invert the runtime movement updating evaluation flag for cheat triggers."""
        self.frozen = not self.frozen
