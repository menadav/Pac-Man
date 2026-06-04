import json
from pathlib import Path
from typing import List, Optional, Tuple

import pygame

from src.engine.scene import BaseScene
from src.parse.models import HighScoreEntry


class GameOver(BaseScene):
    """End-game overlay scene for processing victory/defeat scenarios and player records."""
    def __init__(self, screen: pygame.Surface, path: str) -> None:
        """Initialize the final scene state tracker, filesystem score paths, and fonts."""
        super().__init__(screen)
        self.path: str = path
        self.player_name: str = ""
        self.check: str = ""
        self.font = pygame.font.Font(None, 100)
        self.score: int = 0

    def checker(self, check: str, highscor: int) -> None:
        """Set the ending condition state and track the achieved end-game score."""
        self.check = check
        self.score = highscor

    def save_highscore(self, name: str, highscore: int) -> None:
        """Persist, rank, and truncate the top 10 player scoreboard records inside a JSON file."""
        file_path = Path(self.path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        scores_list: List[HighScoreEntry] = []
        if file_path.exists():
            try:
                data = json.loads(file_path.read_text(encoding="utf-8"))
                scores_list = [HighScoreEntry(**item) for item in data]
            except (json.JSONDecodeError, IOError, PermissionError, TypeError):
                scores_list = []
        try:
            scores_list.append(HighScoreEntry(name=name, score=highscore))
        except ValueError as exc:
            print(f"[HIGHSCORE WARNING] Invalid entry skipped: {exc}")
            return
        scores_list.sort(key=lambda x: x.score, reverse=True)
        top_scores = scores_list[:10]
        json_data = [entry.model_dump() for entry in top_scores]
        try:
            file_path.write_text(json.dumps(json_data, indent=4), encoding="utf-8")
        except IOError:
            print(f"[HIGHSCORE WARNING] Could not write to {self.path}")

    def handle_events(
        self, events: List[pygame.event.Event]
    ) -> Optional[Tuple[str, int]]:
        """Process keyboard name entry strings and trigger structural validation on return."""
        for event in events:
            if event.type == pygame.QUIT:
                return ("QUIT", 0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(self.player_name) > 0:
                    self.save_highscore(self.player_name, self.score)
                    self.player_name = ""
                    return ("MENU", 0)
                if event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif len(self.player_name) < 10:
                    if event.unicode.isalnum() or event.unicode == " ":
                        self.player_name += event.unicode
        return None

    @staticmethod
    def _render_scaled(
        text: str, color: Tuple[int, int, int], target_h: int
    ) -> pygame.Surface:
        """Render a raw text element and structurally scale it to a target height."""
        base = pygame.font.Font(None, 100).render(text, True, color)
        scale = target_h / max(1, base.get_height())
        return pygame.transform.scale_by(base, scale)

    def draw(self, screen: pygame.Surface) -> None:
        """Render dynamic title variants, scores, name inputs, and baseline hint labels."""
        screen.fill((0, 0, 0))
        sw, sh = screen.get_size()
        center_x = sw // 2
        if self.check == "WIN":
            title_str = "VICTORY"
            title_color = (0, 255, 0)
        else:
            title_str = "GAME OVER"
            title_color = (255, 0, 0)
        title = self._render_scaled(title_str, title_color, int(sh * 0.13))
        screen.blit(title, title.get_rect(center=(center_x, int(sh * 0.18))))
        score = self._render_scaled(
            f"SCORE: {self.score}", (255, 255, 255), int(sh * 0.08)
        )
        screen.blit(score, score.get_rect(center=(center_x, int(sh * 0.34))))
        label = self._render_scaled("Enter your name:", (200, 200, 200), int(sh * 0.06))
        screen.blit(label, label.get_rect(center=(center_x, int(sh * 0.50))))
        display_name = self.player_name
        if len(self.player_name) < 10:
            display_name += "_"
        name = self._render_scaled(
            display_name if display_name else "_",
            (255, 255, 0),
            int(sh * 0.07),
        )
        screen.blit(name, name.get_rect(center=(center_x, int(sh * 0.60))))
        rules = self._render_scaled(
            "10 chars max - letters, digits and spaces only",
            (120, 120, 120),
            int(sh * 0.035),
        )
        screen.blit(rules, rules.get_rect(center=(center_x, int(sh * 0.70))))
        if len(self.player_name) > 0:
            hint = self._render_scaled(
                "Press ENTER to save", (150, 150, 150), int(sh * 0.04)
            )
            screen.blit(hint, hint.get_rect(center=(center_x, int(sh * 0.80))))
