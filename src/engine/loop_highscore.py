import pygame
from typing import Optional, List, Tuple
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

    def handle_events(self, events: List[pygame.event.Event]) -> Optional[Tuple[str, int]]:
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
            return ("GAME", 0)
        elif option == "Back to menu":
            return ("MENU", 0)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((0, 0, 0))
        sw, sh = screen.get_size()
        center_x = sw // 2
        title_surf = self.font.render("PAC-MAN", True, (255, 255, 0))
        t_scale = (sh * 0.10) / title_surf.get_height() 
        title_surf = pygame.transform.scale_by(title_surf, t_scale)
        screen.blit(title_surf, title_surf.get_rect(center=(center_x, sh * 0.10)))
        menu_base_y = sh * 0.25
        menu_spacing = sh * 0.07 
        for i, option in enumerate(self.option):
            color = (255, 255, 0) if i == self.index else (255, 255, 255)
            surf = self.font.render(option, True, color)
            s_scale = (sh * 0.05) / surf.get_height()
            surf = pygame.transform.scale_by(surf, s_scale)
            screen.blit(surf, surf.get_rect(center=(center_x, menu_base_y + i * menu_spacing)))
        if not self.score_list:
            empty_surf = self.font.render("Cargando puntajes...", True, (100, 100, 100))
            screen.blit(empty_surf, empty_surf.get_rect(center=(center_x, sh * 0.60)))
        else:
            scores_base_y = sh * 0.45
            scores_spacing = sh * 0.05 
            for j, line in enumerate(self.score_list):
                color = (0, 255, 255) if line == "Highscores" else (200, 200, 200)
                score_surf = self.font.render(line, True, color)
                score_scale = (sh * 0.04) / score_surf.get_height()
                score_surf = pygame.transform.scale_by(score_surf, score_scale)
                rect = score_surf.get_rect(center=(center_x, scores_base_y + j * scores_spacing))
                if rect.bottom < sh:
                    screen.blit(score_surf, rect)
