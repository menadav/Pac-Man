import pygame
import json
from pathlib import Path
from typing import List, Optional
from src.engine.scene import BaseScene
from src.parse.models import HighScoreEntry

class GameOver(BaseScene):
    def __init__(self, screen: pygame.Surface, path: str) -> None:
        super().__init__(screen)
        self.path: str = path
        self.player_name: str = ""
        self.check: str = ""
        self.font = pygame.font.Font(None, 100)
        self.score: int = 0

    def checker(self, check: str, highscor: int) -> None:
        self.check = check
        self.score = highscor

    def save_highscore(self, name: str, highscore: int) -> None:
        file_path = Path(self.path)
        scores_list: List[HighScoreEntry] = []
        if file_path.exists():
            try:
                data = json.loads(file_path.read_text(encoding='utf-8'))
                scores_list = [HighScoreEntry(**item) for item in data]
            except (json.JSONDecodeError, IOError, PermissionError):
                scores_list = []
        try:
            new_entry = HighScoreEntry(name=name, score=highscore)
            scores_list.append(new_entry)
        except ValueError as e:
            raise ValueError(f"Invalid entry skipped: {e}")
        scores_list.sort(key=lambda x: x.score, reverse=True)
        top_scores = scores_list[:10]
        json_data = [entry.model_dump() for entry in top_scores]
        try:
            file_path.write_text(json.dumps(json_data, indent=4), encoding='utf-8')
        except IOError:
            raise ValueError("[ERROR] Could not write to highscore file at {self.path}")

    def handle_events(self, events: List[pygame.event.Event]) -> Optional[str]:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(self.player_name) > 0:
                    self.save_highscore(self.player_name, self.score)
                    self.player_name = ""
                    return ("MENU", 0)
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif len(self.player_name) < 10:
                    if event.unicode.isalnum() or event.unicode == " ":
                        self.player_name += event.unicode
        return None

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((0, 0, 0))
        if self.check == "WIN":
            title_str = "VICTORY"
            title_color = (0, 255, 0)
        else:
            title_str = "GAME OVER"
            title_color = (255, 0, 0)
        title_surf = self.font.render(title_str, True, title_color)
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title_surf, title_rect)
        score_font = pygame.font.Font(None, 70)
        score_surf = score_font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(screen.get_width() // 2, 220))
        screen.blit(score_surf, score_rect)
        input_font = pygame.font.Font(None, 50)
        label_surf = input_font.render("Enter your name:", True, (200, 200, 200))
        label_rect = label_surf.get_rect(center=(screen.get_width() // 2, 350))
        screen.blit(label_surf, label_rect)
        display_name = self.player_name
        if len(self.player_name) < 10:
            display_name += "_"      
        name_surf = input_font.render(display_name, True, (255, 255, 0))
        name_rect = name_surf.get_rect(center=(screen.get_width() // 2, 400))
        screen.blit(name_surf, name_rect)
        if len(self.player_name) > 0:
            hint_surf = pygame.font.Font(None, 30).render("Press ENTER to save", True, (150, 150, 150))
            hint_rect = hint_surf.get_rect(center=(screen.get_width() // 2, 550))
            screen.blit(hint_surf, hint_rect)