import pygame
from typing import List, Optional
from src.parse.models import HighScoreEntry
from src.engine.scene import BaseScene


class Menu(BaseScene):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.index = 0
        self.options = ["Start", "Highscores", "Instructions", "Exit"]
        self.font = pygame.font.Font(None, 127)


    def handle_events(self, events: List[str]) -> Optional[str]:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.index = (self.index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.index = (self.index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.select_options()
        return None

    def draw(self, screen):
        screen.fill((0, 0, 0))
        center_x = screen.get_width() // 2
        title_surf = self.font.render("PAC-MAN", True, (255, 255, 0))
        title_surf = pygame.transform.scale_by(title_surf, 1.965)
        title_rect = title_surf.get_rect(center=(center_x, 120))
        screen.blit(title_surf, title_rect)
        menu_start_y = 350
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.index else (255, 255, 255)
            surf = self.font.render(option, True, color)
            screen.blit(surf, surf.get_rect(center=(center_x, menu_start_y + i * 140)))

    def select_options(self) -> str:
        option = self.options[self.index]
        if option == "Start":
            return "GAME"
        elif option == "Highscores":
            return "HIGHSCORES"
        elif option == "Instructions":
            return "INSTRUCTIONS"
        elif option == "Exit":
            return "QUIT"
