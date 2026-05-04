import pygame
from typing import Optional, List
from src.parse.models import HighScoreEntry
from src.engine.scene import BaseScene

class HighScoreScene(BaseScene):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.index = 0
        self.option = ["Play", "Back to menu"]
        self.font = pygame.font.Font(None, 100)
        self.score_list = []

    def high_load(self, data:Optional[List[HighScoreEntry]]) -> None:
        if not data:
            self.score_list = ["The score is empty"]
            return
        scores: List[str] = []
        scores.append("Highscores")
        data_sort = sorted(data, key=lambda x: x.score, reverse=True)[:10]
        for i, entry in enumerate(data_sort):
            line = f"{i + 1}.{entry.name}-{entry.score}pts"
            scores.append(line)
        self.score_list = scores

    def handle_events(self, events: List[str]) -> Optional[str]:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                        self.index = (self.index - 1) % len(self.option)
                elif event.key == pygame.K_DOWN:
                    self.index = (self.index + 1) % len(self.option)
                elif event.key == pygame.K_RETURN:
                    return self.select_options()

    def select_options(self) -> str:
        option = self.option[self.index]
        if option == "Play":
            return "GAME"
        elif option == "Back to menu":
            return "MENU"

    def draw(self, screen):
        screen.fill((0, 0, 0))
        center_x = screen.get_width() // 2
        title_surf = self.font.render("PAC-MAN", True, (255, 255, 0))
        title_surf = pygame.transform.scale_by(title_surf, 2.5)
        title_rect = title_surf.get_rect(center=(center_x, 120))
        screen.blit(title_surf, title_rect)
        menu_start_y = 350
        for i, option in enumerate(self.option):
            color = (255, 255, 0) if i == self.index else (255, 255, 255)
            surf = self.font.render(option, True, color)
            screen.blit(surf, surf.get_rect(center=(center_x, menu_start_y + i * 140)))
        scores_start_y = 650 
        for j, line in enumerate(self.score_list):
            surf = self.font.render(line, True, (255, 255, 255))
            rect = surf.get_rect(center=(center_x, scores_start_y + j * 90))
            screen.blit(surf, rect)
