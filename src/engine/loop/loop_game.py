import math
from typing import List, Optional, Tuple

import pygame

from src.engine.direction import CONTROLS, Direction
from src.engine.scene import BaseScene
from src.entities.entitiesmannager import EntitiesMannager
from src.parse.models import ParseConfig

GHOST_COLORS = {
    "Blinky": (255, 0, 0),
    "Pinky": (255, 182, 193),
    "Inky": (0, 255, 255),
    "Clyde": (255, 165, 0),
}
GHOST_ESCAPE_COLOR = (33, 33, 222)
GHOST_ESCAPE_BLINK = (240, 240, 240)


class GameRun(BaseScene):
    """Main gameplay runtime scene driving clock iterations, updates, and asset rendering."""
    GAME_TICK_HZ = 60

    def __init__(self, screen: pygame.Surface, data: ParseConfig) -> None:
        super().__init__(screen)
        self.options = ["CONTINUE", "CHEAT", "MENU"]
        self.index = 0
        self.screen = screen
        self.data = data
        self.game_mannager = EntitiesMannager(self.data, self.screen)
        self.font = pygame.font.Font(None, 100)
        self.WATCH = pygame.USEREVENT + 1
        pygame.time.set_timer(self.WATCH, 1000)
        self._update_accum_ms: float = 0.0
        self._last_update_ms: int = pygame.time.get_ticks()

    def update(self) -> None:
        """Process delta time accumulations and execute sub-step framework physics updates."""
        now = pygame.time.get_ticks()
        elapsed = now - self._last_update_ms
        self._last_update_ms = now
        if self.game_mannager.status != "RUNNING":
            self._update_accum_ms = 0.0
            return
        self._update_accum_ms += elapsed
        step_ms = 1000.0 / self.GAME_TICK_HZ
        max_steps = 4
        while self._update_accum_ms >= step_ms and max_steps > 0:
            self.game_mannager.update()
            self._update_accum_ms -= step_ms
            max_steps -= 1

    def handle_events(
        self, events: List[pygame.event.Event]
    ) -> Optional[Tuple[str, int]]:
        """Intercept input vectors, clock increments, and state validation sequences."""
        for event in events:
            if event.type == pygame.QUIT:
                return ("QUIT", 0)
            if event.type == self.WATCH:
                if self.game_mannager.status == "RUNNING":
                    self.game_mannager.update_level_time()
            if event.type == pygame.KEYDOWN:
                if self.game_mannager.status == "RUNNING":
                    if self.game_mannager.player.cheat:
                        if event.key == pygame.K_SPACE:
                            self.game_mannager.next_level()
                        elif event.key in (
                            pygame.K_PLUS,
                            pygame.K_KP_PLUS,
                            pygame.K_EQUALS,
                        ):
                            if self.game_mannager.player.live < 10:
                                self.game_mannager.player.live += 1
                        elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                            self.game_mannager.player.live -= 1
                        elif event.key == pygame.K_f:
                            self.game_mannager.ghost_mannager.toggle_freeze()
                    if event.key in CONTROLS:
                        new_dir = CONTROLS[event.key]
                        self.game_mannager.player.direction(new_dir)
                    if event.key == pygame.K_ESCAPE:
                        self.game_mannager.status = "PAUSE"
                elif self.game_mannager.status == "PAUSE":
                    if event.key == pygame.K_UP:
                        self.index = (self.index - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.index = (self.index + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        return self.select_options()
                    elif event.key == pygame.K_ESCAPE:
                        self.game_mannager.status = "RUNNING"
            if self.game_mannager.status == "WIN":
                return ("WIN", self.game_mannager.score)
            elif self.game_mannager.status == "END":
                return ("END", self.game_mannager.score)
        return None

    def select_options(self) -> Optional[Tuple[str, int]]:
        """Map highlighted pause screen index parameters to programmatic state flags."""
        option = self.options[self.index]
        if option == "MENU":
            return ("MENU", 0)
        if option == "CHEAT":
            self.game_mannager.player.cheat_mode()
        if option == "CONTINUE":
            self.game_mannager.status = "RUNNING"
        return None

    def draw(self, screen: pygame.Surface) -> None:
        """Render active maze matrices, characters, heads-up dashboards, and menu overlays."""
        screen.fill((0, 0, 0))
        current_lvl = self.game_mannager.current_level
        if current_lvl.width == 0 or current_lvl.height == 0:
            return

        tile_size = self.game_mannager.t_size
        offset_x, offset_y = self.game_mannager.get_centering_offsets()

        self._draw_hud(screen)
        self._draw_maze(screen, tile_size, offset_x, offset_y)
        self._draw_player(screen, tile_size, offset_x, offset_y)
        self._draw_ghosts(screen, tile_size, offset_x, offset_y)

        time_left = self.game_mannager.level_time
        if 0 < time_left <= 5:
            alpha = 60 + (pygame.time.get_ticks() // 200) % 2 * 40
            scrim = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            scrim.fill((255, 0, 0, alpha))
            screen.blit(scrim, (0, 0))

        if self.game_mannager.status == "PAUSE":
            self._draw_pause_overlay(screen)

    def _draw_hud(self, screen: pygame.Surface) -> None:
        """Render operational metrics dashboards, text flags, and remaining lives symbols."""
        sw = screen.get_width()
        hud_h = self.game_mannager.hud_height()
        pygame.draw.line(screen, (40, 40, 80), (0, hud_h - 2), (sw, hud_h - 2), 2)

        font_size = max(20, int(hud_h * 0.55))
        font = pygame.font.Font(None, font_size)

        player = self.game_mannager.player
        score = self.game_mannager.score
        lives = max(0, player.live)
        level_idx = self.game_mannager.level_index + 1
        total_lvls = len(self.data.levels)
        time_left = max(0, self.game_mannager.level_time)

        score_surf = font.render(f"SCORE  {score:06d}", True, (255, 255, 255))
        level_surf = font.render(
            f"LEVEL  {level_idx}/{total_lvls}", True, (255, 255, 0)
        )
        if time_left > 30:
            time_color = (180, 220, 255)
            time_font = font
        elif time_left > 10:
            time_color = (255, 200, 80)
            time_font = font
        else:
            pulse = (pygame.time.get_ticks() // 250) % 2 == 0
            time_color = (255, 60, 60) if pulse else (255, 200, 60)
            time_font = pygame.font.Font(None, int(font_size * 1.5))
        time_surf = time_font.render(f"TIME  {time_left:02d}s", True, time_color)
        lives_label = font.render("LIVES", True, (255, 255, 255))

        y = hud_h // 2
        margin = int(sw * 0.02)

        screen.blit(score_surf, score_surf.get_rect(midleft=(margin, y)))
        screen.blit(level_surf, level_surf.get_rect(center=(sw // 2, y)))
        screen.blit(time_surf, time_surf.get_rect(midright=(sw - margin - 1, y)))

        icon_r = max(6, int(hud_h * 0.20))
        block_w = lives_label.get_width() + 10 + lives * (icon_r * 2 + 6)
        lives_x = int(sw * 0.68) - block_w // 2
        screen.blit(lives_label, lives_label.get_rect(midleft=(lives_x, y)))
        cx = lives_x + lives_label.get_width() + 12 + icon_r
        for _ in range(lives):
            self._draw_pacman_icon(screen, (cx, y), icon_r)
            cx += icon_r * 2 + 6

        if player.cheat:
            cheat_font = pygame.font.Font(None, max(18, font_size - 8))
            cheat = cheat_font.render("CHEAT MODE", True, (0, 255, 120))
            screen.blit(cheat, cheat.get_rect(midleft=(margin, hud_h - 12)))

    @staticmethod
    def _draw_pacman_icon(
        screen: pygame.Surface, center: Tuple[int, int], radius: int
    ) -> None:
        """Draw an isolated static profile vector icon for scoreboard live trackers."""
        pygame.draw.circle(screen, (255, 255, 0), center, radius)
        cx, cy = center
        mouth = [
            (cx, cy),
            (cx + radius, cy - radius // 2),
            (cx + radius, cy + radius // 2),
        ]
        pygame.draw.polygon(screen, (0, 0, 0), mouth)

    def _draw_maze(
        self, screen: pygame.Surface, tile_size: int, offset_x: int, offset_y: int
    ) -> None:
        """Render the primary grid environment layout and pulsing item instances."""
        wall_color = (0, 0, 255)
        yellow = (255, 255, 0)
        pulse = 1.0 + 0.25 * math.sin(pygame.time.get_ticks() / 180.0)
        super_r = max(3, int((tile_size // 3) * pulse))
        for y, row in enumerate(self.game_mannager.matrix):
            for x, cell_value in enumerate(row):
                px = offset_x + (x * tile_size)
                py = offset_y + (y * tile_size)
                cx = px + tile_size // 2
                cy = py + tile_size // 2
                if cell_value & 32:
                    pygame.draw.circle(screen, yellow, (cx, cy), super_r)
                elif cell_value & 16:
                    pygame.draw.circle(screen, yellow, (cx, cy), max(2, tile_size // 8))
                if cell_value & 1:
                    pygame.draw.line(
                        screen, wall_color, (px, py), (px + tile_size, py), 2
                    )
                if cell_value & 2:
                    pygame.draw.line(
                        screen,
                        wall_color,
                        (px + tile_size, py),
                        (px + tile_size, py + tile_size),
                        2,
                    )
                if cell_value & 4:
                    pygame.draw.line(
                        screen,
                        wall_color,
                        (px, py + tile_size),
                        (px + tile_size, py + tile_size),
                        2,
                    )
                if cell_value & 8:
                    pygame.draw.line(
                        screen, wall_color, (px, py), (px, py + tile_size), 2
                    )
    _last_facing: Direction = Direction.RIGHT

    def _draw_player(
        self, screen: pygame.Surface, tile_size: int, offset_x: int, offset_y: int
    ) -> None:
        """Deduce historical rotation angles and draw animated player polygons."""
        player = self.game_mannager.player
        cx = int(offset_x + player.pixel_x + tile_size // 2)
        cy = int(offset_y + player.pixel_y + tile_size // 2)
        radius = max(3, tile_size // 2 - 2)

        dir_angles = {
            Direction.RIGHT: 0,
            Direction.UP: 90,
            Direction.LEFT: 180,
            Direction.DOWN: 270,
        }
        if player.current_direction in dir_angles:
            self._last_facing = player.current_direction
        facing = self._last_facing
        base_angle = dir_angles.get(facing, 0)

        is_moving = player.current_direction in dir_angles
        if is_moving:
            t = pygame.time.get_ticks() / 110.0
            opening_deg = 8 + 32 * (0.5 + 0.5 * math.cos(t))
        else:
            opening_deg = 8

        self._draw_pacman_sprite(screen, (cx, cy), radius, base_angle, opening_deg)

    @staticmethod
    def _draw_pacman_sprite(
        screen: pygame.Surface,
        center: Tuple[int, int],
        radius: int,
        base_angle_deg: float,
        opening_deg: float,
    ) -> None:
        """Render a modular chomp-animated polygon representation for Pacman."""
        cx, cy = center
        body = (255, 230, 0)
        outline = (210, 170, 0)
        n_arc = 36
        start = math.radians(base_angle_deg + opening_deg)
        end = math.radians(base_angle_deg - opening_deg + 360)
        points: List[Tuple[int, int]] = [(cx, cy)]
        for i in range(n_arc + 1):
            a = start + (end - start) * i / n_arc
            points.append(
                (
                    int(cx + radius * math.cos(a)),
                    int(cy - radius * math.sin(a)),
                )
            )
        pygame.draw.polygon(screen, body, points)
        pygame.draw.polygon(screen, outline, points, 2)
        eye_r = max(2, radius // 6)
        eye_dist = radius * 0.45
        eye_angle = math.radians(base_angle_deg + 70)
        ex = int(cx + eye_dist * math.cos(eye_angle))
        ey = int(cy - eye_dist * math.sin(eye_angle))
        pygame.draw.circle(screen, (30, 30, 30), (ex, ey), eye_r)

    _DIR_OFFSETS = {
        Direction.RIGHT: (1, 0),
        Direction.LEFT: (-1, 0),
        Direction.UP: (0, -1),
        Direction.DOWN: (0, 1),
    }

    def _draw_ghosts(
        self, screen: pygame.Surface, tile_size: int, offset_x: int, offset_y: int
    ) -> None:
        """Process visual statuses, floating bob animations, and draw ghosts collections."""
        time_escape = self.game_mannager.ghost_mannager.time_escape
        level_time = self.game_mannager.level_time
        blink_now = (
            isinstance(time_escape, (int, float))
            and time_escape != float("inf")
            and (level_time - time_escape) <= 3
            and (pygame.time.get_ticks() // 200) % 2 == 0
        )

        radius = max(4, tile_size // 2 - 1)
        bob_base = math.sin(pygame.time.get_ticks() / 220.0) * max(1, radius // 8)

        for i, ghost in enumerate(self.game_mannager.ghost_mannager.ghosts):
            cx = int(offset_x + ghost.pixel_x + tile_size // 2)
            cy = int(
                offset_y
                + ghost.pixel_y
                + tile_size // 2
                + bob_base * (1 if i % 2 == 0 else -1)
            )
            if ghost.mode == "EATEN":
                self._draw_ghost_eyes(screen, (cx, cy), radius, ghost.current_direction)
                continue
            name = ghost.__class__.__name__
            if ghost.mode == "ESCAPE":
                color = GHOST_ESCAPE_BLINK if blink_now else GHOST_ESCAPE_COLOR
            else:
                color = GHOST_COLORS.get(name, (255, 255, 255))
            self._draw_ghost_sprite(
                screen, (cx, cy), radius, color, ghost.mode, ghost.current_direction
            )

    @classmethod
    def _draw_ghost_sprite(
        cls,
        screen: pygame.Surface,
        center: Tuple[int, int],
        radius: int,
        color: Tuple[int, int, int],
        mode: str,
        direction: Direction,
    ) -> None:
        """Build and render complete scaled multi-scallop body vectors for individual ghosts."""
        cx, cy = center
        outline = (max(0, color[0] - 60), max(0, color[1] - 60), max(0, color[2] - 60))
        outline_w = max(1, radius // 10)

        body_bottom_y = cy + radius
        n_arc = 24
        n_scallops = 3
        scallop_w = (2 * radius) / n_scallops
        scallop_dip = scallop_w * 0.45

        points: List[Tuple[float, float]] = []
        for i in range(n_arc + 1):
            a = math.pi - math.pi * i / n_arc
            x = cx - radius * math.cos(a)
            y = cy - radius * math.sin(a)
            points.append((x, y))
        points.append((cx + radius, body_bottom_y))
        for i in range(n_scallops):
            x_right = cx + radius - i * scallop_w
            x_mid = x_right - scallop_w / 2
            x_left = x_right - scallop_w
            points.append((x_mid, body_bottom_y - scallop_dip))
            points.append((x_left, body_bottom_y))
        points.append((cx - radius, cy))
        int_points = [(int(x), int(y)) for x, y in points]
        pygame.draw.polygon(screen, color, int_points)
        pygame.draw.polygon(screen, outline, int_points, outline_w)

        if mode == "ESCAPE":
            cls._draw_scared_face(screen, (cx, cy), radius)
        else:
            cls._draw_ghost_eyes(screen, (cx, cy), radius, direction)

    @classmethod
    def _draw_ghost_eyes(
        cls,
        screen: pygame.Surface,
        center: Tuple[int, int],
        radius: int,
        direction: Direction,
    ) -> None:
        """Render directional shifting eye and pupil surfaces inside active ghost outlines."""
        cx, cy = center
        eye_r = max(3, int(radius * 0.30))
        pupil_r = max(2, int(eye_r * 0.55))
        eye_off_x = int(radius * 0.40)
        eye_off_y = -int(radius * 0.15)
        dx, dy = cls._DIR_OFFSETS.get(direction, (0, 0))
        shift = max(1, pupil_r // 2)
        for sign in (-1, 1):
            ex = cx + sign * eye_off_x
            ey = cy + eye_off_y
            pygame.draw.circle(screen, (255, 255, 255), (ex, ey), eye_r)
            pygame.draw.circle(
                screen,
                (20, 20, 90),
                (ex + dx * shift, ey + dy * shift),
                pupil_r,
            )

    @staticmethod
    def _draw_scared_face(
        screen: pygame.Surface,
        center: Tuple[int, int],
        radius: int,
    ) -> None:
        """Render customized scared expressions for vulnerable ghosts under escape modes."""
        cx, cy = center
        eye_r = max(2, int(radius * 0.18))
        eye_off_x = int(radius * 0.40)
        eye_off_y = -int(radius * 0.10)
        for sign in (-1, 1):
            pygame.draw.circle(
                screen, (255, 255, 255), (cx + sign * eye_off_x, cy + eye_off_y), eye_r
            )
        mouth_y = cy + int(radius * 0.30)
        mouth_w = int(radius * 1.2)
        n = 6
        step = mouth_w // n
        x0 = cx - mouth_w // 2
        amp = max(2, radius // 8)
        points = [
            (x0 + i * step, mouth_y + (amp if i % 2 == 0 else -amp))
            for i in range(n + 1)
        ]
        pygame.draw.lines(screen, (255, 255, 255), False, points, max(1, radius // 10))

    def _draw_pause_overlay(self, screen: pygame.Surface) -> None:
        """Render full-screen semi-transparent backdrops and interactive options for pauses."""
        sw, sh = screen.get_width(), screen.get_height()
        overlay = pygame.Surface((sw, sh), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title = self.font.render("PAUSE", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(sw // 2, sh // 4)))

        start_y = sh // 2
        spacing = max(60, int(sh * 0.10))
        player = self.game_mannager.player
        for i, option in enumerate(self.options):
            selected = i == self.index
            text_color = (255, 255, 0) if selected else (150, 150, 150)
            display_text = option
            if option == "CHEAT" and getattr(player, "cheat", False):
                display_text = "CHEAT: ACTIVE"
                text_color = (0, 255, 255) if selected else (0, 255, 100)
            surf = self.font.render(display_text, True, text_color)
            screen.blit(surf, surf.get_rect(center=(sw // 2, start_y + i * spacing)))
