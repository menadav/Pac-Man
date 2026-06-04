import src.engine.env  # noqa: F401

try:
    import pygame
except ImportError as exc:
    raise ValueError("[ERROR] Install Pygame") from exc

import json
from pathlib import Path
from typing import List, Optional

from src.engine.loop.loop_end import GameOver
from src.engine.loop.loop_game import GameRun
from src.engine.loop.loop_highscore import HighScoreScene
from src.engine.loop.loop_instructions import Instructions
from src.engine.loop.loop_menu import Menu
from src.engine.scene import BaseScene
from src.parse.models import HighScoreEntry, ParseConfig


class GameMannager:
    """Core coordinator managing the central game loop, window states, and scenes."""
    def __init__(self, data: ParseConfig) -> None:
        """Initialize Pygame context, system display settings, and state machine scenes."""
        pygame.init()
        info = pygame.display.Info()
        self.screen = pygame.display.set_mode(
            (info.current_w, info.current_h), pygame.FULLSCREEN
        )
        pygame.display.set_caption("Pac-Man")
        self.scores = data.file
        self.data = data
        self.menu = Menu(self.screen)
        self.game: Optional[GameRun] = None
        self.highscore = HighScoreScene(self.screen)
        self.instructions = Instructions(self.screen)
        self.end = GameOver(self.screen, self.scores)
        self.current_scene: BaseScene = self.menu
        self.running = True
        self.clock = pygame.time.Clock()

    def run(self) -> None:
        """Execute the primary game loop processing events, scene ticks, and rendering."""
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            signal = self.current_scene.handle_events(events)
            if isinstance(signal, tuple):
                self._handle_signal(signal[0], signal[1])
            if self.game is not None and self.current_scene is self.game:
                self.game.update()
            self.current_scene.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def _handle_signal(self, scene_signal: str, score: int) -> None:
        """Route engine state transitions based on operational strings emitted by scenes."""
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
        elif scene_signal in ("END", "WIN"):
            self.end.checker(scene_signal, score)
            self.current_scene = self.end
        elif scene_signal == "QUIT":
            self.running = False

    @staticmethod
    def load_score(scores: str) -> Optional[List[HighScoreEntry]]:
        """Load and parse high score entries safely from a JSON storage destination."""
        path = Path(scores)
        if not path.exists():
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [HighScoreEntry(**item) for item in data]
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            return []
