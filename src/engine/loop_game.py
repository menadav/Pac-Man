import pygame
from typing import List, Optional, Tuple
from src.engine.controls import CONTROLS, Direction
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
        self.screen = screen
        self.data = data
        self.game_mannager = EntitiesMannager(self.data)
        self.score = 0
        self.font = pygame.font.Font(None, 100)

    def update(self) -> None:
        self.game_mannager.update()

    def handle_events(
            self, events: List[pygame.event.Event]
            ) -> Optional[Tuple[str, int]]:
        for event in events:
            if event.type == pygame.QUIT:
                return ("QUIT", self.score)
            if event.type == pygame.KEYDOWN:
                if event.key in CONTROLS:
                    new_dir = CONTROLS[event.key]
                    self.game_mannager.player.direction(new_dir)
            if self.game_mannager.status == "WIN":
                return ("WIN", self.score)
            elif self.game_mannager.status == "END":
                return("END", self.score)
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
        p_x, p_y = self.game_mannager.player.current_zone
        player_center_x = p_x * tile_size + tile_size // 2
        player_center_y = p_y * tile_size + tile_size // 2
        pygame.draw.circle(
            screen, 
            (255, 255, 0),
            (player_center_x, player_center_y), 
            tile_size // 2 - 2
        )