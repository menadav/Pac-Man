from typing import List, Optional, Tuple

import pygame

from src.engine.scene import BaseScene

INSTRUCTIONS_TEXT: List[Tuple[str, Tuple[int, int, int]]] = [
    ("CONTROLS", (0, 255, 255)),
    ("Arrow keys or WASD : move Pac-Man", (255, 255, 255)),
    ("ESC                : pause / resume the game", (255, 255, 255)),
    ("", (0, 0, 0)),
    ("GOAL", (0, 255, 255)),
    ("Eat every pacgum to clear the level", (255, 255, 255)),
    ("Avoid the ghosts - they take one life on contact", (255, 255, 255)),
    ("Super-pacgums (corners) let you eat ghosts briefly", (255, 255, 255)),
    ("Watch the TIME in the HUD: running out costs a life", (255, 200, 80)),
    ("and restarts the level (game over only at 0 lives)", (255, 200, 80)),
    ("", (0, 0, 0)),
    ("CHEAT MODE (for peer review)", (0, 255, 120)),
    ("Open the pause menu and pick CHEAT to toggle it.", (200, 200, 200)),
    ("When active:", (200, 200, 200)),
    ("  - Invincibility (ghosts cannot kill you)", (200, 200, 200)),
    ("  - SPACE          : skip the current level", (200, 200, 200)),
    ("  - +  /  -        : add or remove a life", (200, 200, 200)),
    ("  - F              : freeze / unfreeze the ghosts", (200, 200, 200)),
    ("  - Pac-Man moves at double speed", (200, 200, 200)),
    ("  - Timer auto-refills when it would hit zero", (200, 200, 200)),
    ("", (0, 0, 0)),
    ("Press ENTER to return to the main menu", (255, 255, 0)),
]


class Instructions(BaseScene):
    """Instructions overlay state presenting game commands and cheat codes."""
    def __init__(self, screen: pygame.Surface) -> None:
        """Initialize the instructions scene, fonts, and baseline options."""
        super().__init__(screen)
        self.font = pygame.font.Font(None, 100)
        self.options = ["Return"]

    def handle_events(
        self, events: List[pygame.event.Event]
    ) -> Optional[Tuple[str, int]]:
        """Intercept confirmation keystrokes to redirect users back to the main menu."""
        for event in events:
            if event.type == pygame.QUIT:
                return ("QUIT", 0)
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    return ("MENU", 0)
        return None

    def draw(self, screen: pygame.Surface) -> None:
        """Draw and dynamically resize instructions and text configurations. """
        screen.fill((0, 0, 0))
        sw, sh = screen.get_size()
        center_x = sw // 2

        title_surf = self.font.render("INSTRUCTIONS", True, (255, 255, 0))
        t_scale = (sh * 0.10) / title_surf.get_height()
        title_surf = pygame.transform.scale_by(title_surf, t_scale)
        screen.blit(
            title_surf,
            title_surf.get_rect(center=(center_x, int(sh * 0.10))),
        )

        start_y = sh * 0.22
        line_h = sh * 0.045
        line_font = pygame.font.Font(None, max(20, int(sh * 0.05)))
        for i, (line, color) in enumerate(INSTRUCTIONS_TEXT):
            if not line:
                continue
            surf = line_font.render(line, True, color)
            if surf.get_width() > sw * 0.9:
                ratio = (sw * 0.9) / surf.get_width()
                surf = pygame.transform.scale_by(surf, ratio)
            screen.blit(
                surf,
                surf.get_rect(center=(center_x, int(start_y + i * line_h))),
            )
