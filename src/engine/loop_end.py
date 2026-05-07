import pygame
from typing import List, Optional
from src.engine.scene import BaseScene

class GameOver(BaseScene):
    def __init__(self, screen: pygame.Surface, path: str) -> None:
        super().__init__(screen)
        self.path: str = path
        self.player_name: str = ""
        self.check: str = ""
        self.score: int = 0

    def checker(self, check: str, highscor: int) -> None:
        self.check = check
        self.score = highscor

    def save_highscore(self, name: str, highscore: int) -> None:
        pass

    def handle_events(self, events: List[pygame.event.Event]) -> Optional[str]:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(self.player_name) > 0:
                    self.save_highscore(self.player_name, self.score)
                    return "MENU"
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif len(self.player_name) < 10:
                    if event.unicode.isalnum() or event.unicode == " ":
                        self.player_name += event.unicode
        return None

    def draw(self, screen: pygame.Surface) -> None:
        pass