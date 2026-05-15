import pygame
from typing import List, Optional, Tuple
from src.engine.direction import CONTROLS
from src.engine.scene import BaseScene
from src.parse.models import ParseConfig
from src.entities.entitiesmannager import EntitiesMannager


class GameRun(BaseScene):
    def __init__(
            self,
            screen: pygame.Surface,
            data: ParseConfig
            ) -> None:
        super().__init__(screen)
        self.options = ["MENU", "CHEAT", "CONTINUE"]
        self.index = 0
        self.screen = screen
        self.data = data
        lvl = self.data.levels[0]
        t_size = min(
            self.screen.get_width()
            // lvl.width, self.screen.get_height() // lvl.height
            )
        self.game_mannager = EntitiesMannager(self.data, t_size)
        self.font = pygame.font.Font(None, 100)
        self.WATCH = pygame.USEREVENT + 1
        pygame.time.set_timer(self.WATCH, 1000)

    def update(self) -> None:
        if self.game_mannager.status == "RUNNING":
            self.game_mannager.update()
        else:
            pass

    def handle_events(
            self, events: List[pygame.event.Event]
            ) -> Optional[Tuple[str, int]]:
        for event in events:
            if event.type == pygame.QUIT:
                return ("QUIT", 0)
            if event.type == self.WATCH:
                self.game_mannager.update_level_time()
            if event.type == pygame.KEYDOWN:
                if self.game_mannager.status == "RUNNING":
                    if self.game_mannager.player.cheat:
                        if event.key == pygame.K_SPACE:
                            self.game_mannager.next_level()
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
            if self.game_mannager.status == "WIN":
                return ("WIN", self.game_mannager.score)
            elif self.game_mannager.status == "END":
                return ("END", self.game_mannager.score)
        return None

    def select_options(self) -> Optional[Tuple[str, int]]:
        option = self.options[self.index]
        if option == "MENU":
            return ("MENU", 0)
        if option == "CHEAT":
            self.game_mannager.player.cheat_mode()
        if option == "CONTINUE":
            self.game_mannager.status = "RUNNING"
        return None

    def draw(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))
        current_lvl = self.game_mannager.current_level
        if current_lvl.width == 0 or current_lvl.height == 0:
            return
        tile_w = screen.get_width() // current_lvl.width
        tile_h = screen.get_height() // current_lvl.height
        tile_size = min(tile_w, tile_h)
        for y, row in enumerate(self.game_mannager.matrix):
            for x, cell_value in enumerate(row):
                px = x * tile_size
                py = y * tile_size
                color = (0, 0, 255)
                center_x = px + tile_size // 2
                center_y = py + tile_size // 2
                yellow = (255, 255, 0)
                if cell_value & 16:
                    pygame.draw.circle(screen, yellow, (center_x, center_y), tile_size // 8)
                elif cell_value & 32:
                    pygame.draw.circle(screen, yellow, (center_x, center_y), tile_size // 3)
                if cell_value & 1:
                    pygame.draw.line(screen, color, (px, py), (px + tile_size, py), 2)
                if cell_value & 2:
                    pygame.draw.line(screen, color, (px + tile_size, py), (px + tile_size, py + tile_size), 2)
                if cell_value & 4:
                    pygame.draw.line(screen, color, (px, py + tile_size), (px + tile_size, py + tile_size), 2)
                if cell_value & 8:
                    pygame.draw.line(screen, color, (px, py), (px, py + tile_size), 2)
        player = self.game_mannager.player
        player_center_x = int(player.pixel_x + tile_size // 2)
        player_center_y = int(player.pixel_y + tile_size // 2)
        pygame.draw.circle(screen, (255, 255, 0), (player_center_x, player_center_y), tile_size // 2 - 2)
        ghost_colors = {
            "Blinky": (255, 0, 0), "Pinky": (255, 182, 193),
            "Inky": (0, 255, 255), "Clyde": (255, 165, 0)
        }
        for ghost in self.game_mannager.ghost_mannager.ghosts:
            gx = ghost.pixel_x
            gy = ghost.pixel_y
            name = ghost.__class__.__name__
            color = ghost_colors.get(name, (255, 255, 255))
            ghost_center = (int(gx + tile_size // 2), int(gy + tile_size // 2))
            pygame.draw.circle(screen, color, ghost_center, tile_size // 2 - 2)    
            eye_color = (255, 255, 255)
            pygame.draw.circle(screen, eye_color, (ghost_center[0] - 4, ghost_center[1] - 2), 2)
            pygame.draw.circle(screen, eye_color, (ghost_center[0] + 4, ghost_center[1] - 2), 2)
        if self.game_mannager.status == "PAUSE":
            overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            title_text = self.font.render("PAUSE", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))
            screen.blit(title_text, title_rect)
            start_y = screen.get_height() // 2
            spacing = 90
            for i, option in enumerate(self.options):
                if i == self.index:
                    text_color = (255, 255, 0)
                else:
                    text_color = (150, 150, 150)
                if option == "CHEAT" and getattr(player, 'cheat', False):
                    text_color = (0, 255, 100) if i != self.index else (0, 255, 255)
                display_text = option
                if option == "CHEAT" and getattr(player, 'cheat', False):
                    display_text = "CHEAT: ACTIVE"
                option_surf = self.font.render(display_text, True, text_color)
                option_rect = option_surf.get_rect(center=(screen.get_width() // 2, start_y + i * spacing))
                screen.blit(option_surf, option_rect)
