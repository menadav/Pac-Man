import src.engine.env
try:
    import pygame
except ImportError:
    raise ValueError("[ERROR] Install Pygame")
import json
from pathlib import Path
from typing import Optional, List
from src.engine.loop.loop_menu import Menu
from src.engine.loop.loop_highscore import HighScoreScene
from src.engine.loop.loop_instructions import Instructions
from src.engine.loop.loop_end import GameOver
from src.engine.loop.loop_game import GameRun
from src.parse.models import ParseConfig, HighScoreEntry


class GameMannager:
    def __init__(self, data: ParseConfig) -> None:
        pygame.init()
        info = pygame.display.Info()
        screen_width = info.current_w
        screen_height = info.current_h
        self.screen = pygame.display.set_mode(
            (screen_width, screen_height), pygame.FULLSCREEN
            )
        self.scores = "src/highscores/highscores.json"
        self.data = data
        self.menu = Menu(self.screen)
        self.game = None
        self.highscore = HighScoreScene(self.screen)
        self.instructions = Instructions(self.screen)
        self.end = GameOver(self.screen, self.scores)
        self.current_scene = self.menu
        self.running = True
        self.clock = pygame.time.Clock()

    def run(self) -> None:
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            signal = self.current_scene.handle_events(events)
            if isinstance(signal, tuple):
                scene_signal = signal[0]
                score = signal[1]
                if scene_signal == "GAME":
                    self.game = GameRun(self.screen, self.data)
                    self.current_scene = self.game
                elif scene_signal == "HIGHSCORES":
                    self.highscore.high_load(self.load_score(self.scores))
                    self.current_scene = self.highscore
                elif scene_signal == "INSTRUCTIONS":
                    self.current_scene = self.instructions
                elif scene_signal == "MENU":
                    self.current_scene = self.menu
                elif scene_signal == "END" or scene_signal == "WIN":
                    self.end.checker(scene_signal, score)
                    self.current_scene = self.end
                elif scene_signal == "QUIT":
                    self.running = False
            if self.current_scene == self.game:
                self.game.update()
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
