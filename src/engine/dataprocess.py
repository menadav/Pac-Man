import src.engine.env
try:
    import pygame
except ImportError:
    raise ValueError("[ERROR] Install Pygame")
import json
from pathlib import Path
from typing import Optional, Dict, List
from src.engine.loop_menu import Menu
from src.engine.loop_highscore import HighScoreScene
from src.engine.loop_instructions import Instructions
from src.parse.models import ParseConfig, HighScoreEntry


class GameMannager:
    def __init__(self, data: ParseConfig) -> None:
        pygame.init()
        info = pygame.display.Info()
        screen_width = info.current_w
        screen_height = info.current_h
        self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        self.scores = self.load_score("src/highscores/highscores.json")
        self.data = data
        self.menu = Menu(self.screen)
        self.highscore = HighScoreScene(self.screen)
        self.instructions = Instructions(self.screen)
        self.current_scene = self.menu
        self.running = True
        self.clock = pygame.time.Clock()

    def run(self) -> None:
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            scene_signal = self.current_scene.handle_events(events)
            if scene_signal == "GAME":
                pass
            elif scene_signal == "HIGHSCORES":
                self.highscore.high_load(self.scores)
                self.current_scene = self.highscore
            elif scene_signal == "INSTRUCTIONS":
                self.current_scene = self.instructions
            elif scene_signal == "MENU":
                self.current_scene = self.menu
            elif scene_signal == "QUIT":
                self.running = False
            self.current_scene.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def load_score(self, scores: str) -> Optional[List[HighScoreEntry]]:
        path = Path(scores)
        if not path.exists():
            return []
        try:
            with open(path, 'r', encoding='utf=8') as f:
                data = json.load(f)
                return [HighScoreEntry(**item) for item in data]
        except (KeyError, TypeError, json.JSONDecodeError):
            return []

