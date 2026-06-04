from typing import Tuple

import pygame
from mazegenerator.mazegenerator import MazeGenerator

from src.engine.direction import Direction
from src.entities.ghost_model.ghostmannager import GhostMannager
from src.entities.items import Items
from src.entities.player import Player
from src.parse.models import ParseConfig


class EntitiesMannager:
    """Orchestrates structural coordination between level , item maps, and character statuses."""
    REDUCTION_FACTOR = 0.90
    HUD_HEIGHT_RATIO = 0.08

    def __init__(self, data: ParseConfig, screen: pygame.Surface) -> None:
        """Initialize operational states, layout boundaries, engine instances, and scores."""
        self.data = data
        self.screen = screen
        self.level_index = 0
        self.bit_superpcgum = 32
        self.bit_pcgum = 16
        self.current_level = self.data.levels[self.level_index]
        self.maze_engine = MazeGenerator(
            size=(self.current_level.width, self.current_level.height),
            seed=self.data.seed,
            perfect=False,
        )
        self.items = Items(self.current_level.pacgum, self.maze_engine.maze)
        self.t_size = self._compute_tile_size()
        self.matrix = self.items.apply_to_matrix()
        ry, rx = self.items.respawn
        self.player = Player((rx, ry), self.data.lives, self.t_size)
        self.lvl_items = len(self.items.pacgums) + len(self.items.super_pacgums)
        self.ghost_mannager = GhostMannager(self.items, self.t_size)
        self.level_time = self.current_level.level_max_time
        self.time_escape = self.level_time + 1
        self.score = 0
        self.status = "RUNNING"

    def next_level(self) -> None:
        """Advance the internal progres index,reload matrices, and scale geometry configurations."""
        self.level_index += 1
        if self.level_index == len(self.data.levels):
            self.status = "WIN"
            return
        remaining_lives = self.player.live
        self.current_level = self.data.levels[self.level_index]
        self.t_size = self._compute_tile_size()
        self.maze_engine = MazeGenerator(
            size=(self.current_level.width, self.current_level.height),
            perfect=False,
        )
        self.items = Items(self.current_level.pacgum, self.maze_engine.maze)
        self.matrix = self.items.apply_to_matrix()
        self.lvl_items = len(self.items.pacgums) + len(self.items.super_pacgums)
        ry, rx = self.items.respawn
        if self.player.cheat:
            self.player = Player((rx, ry), remaining_lives, self.t_size)
            self.player.cheat = True
        else:
            self.player = Player((rx, ry), remaining_lives, self.t_size)
        self.ghost_mannager = GhostMannager(self.items, self.t_size)
        self.level_time = self.current_level.level_max_time
        self.time_escape = self.level_time + 1

    def hud_height(self) -> int:
        """Calculate the exact pixel allowance allocated to the dashboard heads-up display."""
        return int(self.screen.get_height() * self.HUD_HEIGHT_RATIO)

    def _compute_tile_size(self) -> int:
        """Deduce a dynamic, safe uniform tile edge width scaled to fits on display targets."""
        usable_w = self.screen.get_width()
        usable_h = self.screen.get_height() - self.hud_height()
        tile_w = usable_w // self.current_level.width
        tile_h = usable_h // self.current_level.height
        raw = int(min(tile_w, tile_h) * self.REDUCTION_FACTOR)
        return max(6, (raw // 6) * 6)

    def get_centering_offsets(self) -> Tuple[int, int]:
        """Determine horizontal and vertical layout paddings needed to align the active maze."""
        hud = self.hud_height()
        map_w = self.current_level.width * self.t_size
        map_h = self.current_level.height * self.t_size
        usable_h = self.screen.get_height() - hud
        offset_x = (self.screen.get_width() - map_w) // 2
        offset_y = hud + (usable_h - map_h) // 2
        return offset_x, offset_y

    def update_level_time(self) -> None:
        """Decrement level countdown clocks and process time-out life updates safely."""
        if self.status != "RUNNING":
            return
        self.level_time -= 1
        if self.level_time > 0:
            return
        self.level_time = 0
        if self.player.cheat:
            self.level_time = self.current_level.level_max_time
            return
        self.player.live -= 1
        if self.player.live <= 0:
            self.status = "END"
            return
        self._reload_current_level()

    def _reload_current_level(self) -> None:
        """Regenerat and rebuild layout instances for the active lvl without advancing progres."""
        remaining_lives = self.player.live
        was_cheat = self.player.cheat
        self.maze_engine = MazeGenerator(
            size=(self.current_level.width, self.current_level.height),
            perfect=False,
        )
        self.items = Items(self.current_level.pacgum, self.maze_engine.maze)
        self.matrix = self.items.apply_to_matrix()
        self.lvl_items = len(self.items.pacgums) + len(self.items.super_pacgums)
        ry, rx = self.items.respawn
        self.player = Player((rx, ry), remaining_lives, self.t_size)
        self.player.cheat = was_cheat
        self.ghost_mannager = GhostMannager(self.items, self.t_size)
        self.level_time = self.current_level.level_max_time
        self.time_escape = self.level_time + 1

    def can_move(self, current: Tuple[int, int], move: Direction) -> bool:
        """Evaluate if wall mask bitwise parameters allow navigation along targeted vectors."""
        if move == Direction.NONE:
            return False
        x, y = current
        cell_vallue = self.matrix[y][x]
        masks = {
            Direction.UP: 1,
            Direction.RIGHT: 2,
            Direction.DOWN: 4,
            Direction.LEFT: 8,
        }
        return (cell_vallue & masks[move]) == 0

    def update(self) -> None:
        """Drive operational updating steps for item track, directional checks, and ghost tickes."""
        p = self.player
        check = 2 if p.cheat else 1
        for _ in range(check):
            if p.is_centered():
                pos = p.current_zone
                if self.can_move(pos, p.next_direction):
                    p.current_direction = p.next_direction
                if not self.can_move(pos, p.current_direction):
                    p.current_direction = Direction.NONE
                if self._check_bit(pos, self.bit_superpcgum):
                    self._update_bit_score(pos, self.bit_superpcgum)
                elif self._check_bit(pos, self.bit_pcgum):
                    self._update_bit_score(pos, self.bit_pcgum)
                if self._check_lvl():
                    self.next_level()
                    return
            p.update_position()
        self._check_time_super()
        for ghost in self.ghost_mannager.ghosts:
            if ghost.mode == "EATEN":
                ticks = 1
            elif ghost.mode == "ESCAPE":
                ticks = 1
            else:
                ticks = 2
            for _ in range(ticks):
                self.ghost_mannager.update(
                    p.current_zone,
                    p.current_direction,
                    self.can_move,
                    self.level_time,
                    ghost,
                )
        if not self.player.cheat:
            self._check_collision()

    def _check_collision(self) -> None:
        """Perform position verification between entities to enforce damage or points metrics."""
        pos_ghosts = self.ghost_mannager.get_ghost_positions()
        if self.player.current_zone in pos_ghosts:
            if self.player.super and self.ghost_mannager.check_status(
                self.player.current_zone
            ):
                self.ghost_mannager.respawn_ghost(self.player.current_zone)
                self.score += self.data.points_per_ghost
            else:
                self.player.live -= 1
                if self.player.live > 0:
                    self.player.respawn_player()
                    self.ghost_mannager.respawn_ghost()
                else:
                    self.status = "END"

    def _check_lvl(self) -> bool:
        """Evaluate if every required standard and super collection object has been eaten."""
        total_pcgum = self.player.super_pcgum + self.player.pcgum
        if self.lvl_items == total_pcgum:
            return True
        return False

    def _check_bit(self, pos: Tuple[int, int], bit: int) -> bool:
        """Run bitwise validation masks over specific coordinates to check for items."""
        x, y = pos
        return (self.matrix[y][x] & bit) != 0

    def _update_bit_score(self, pos: Tuple[int, int], bit: int) -> None:
        """Strip tracking bits at specified cells and route status score triggers."""
        x, y = pos
        self.matrix[y][x] &= ~bit
        if bit == self.bit_pcgum:
            self.player.pcgum += 1
            self._update_pcgum()
        elif bit == self.bit_superpcgum:
            self.player.super_pcgum += 1
            self._update_superpcgum()

    def _update_pcgum(self) -> None:
        """Add configured baseline pacgum values directly onto global metrics fields."""
        self.score += self.data.points_per_pacgum

    def _update_superpcgum(self) -> None:
        """Add super-pacgum values and initiate associated ghost fleeing conditions."""
        self.score += self.data.points_per_super_pacgum
        self.player.update_super_t()
        self._ghost_superpcgum()

    def _check_time_super(self) -> None:
        """Restore vulnerability behaviors once escape operational timers expire."""
        if self.time_escape > self.level_time:
            self.player.update_super_f()

    def _ghost_superpcgum(self) -> None:
        """Calculate lookahead intervals and command ghosts into escape state routines."""
        self.ghost_mannager.ghost_escape()
        self.time_escape = self.level_time - 8
        if self.time_escape < 0:
            self.ghost_mannager.time_escape = 0
        else:
            self.ghost_mannager.time_escape = self.time_escape
