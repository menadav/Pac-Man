from typing import List, Optional, Tuple

import pygame

from src.engine.scene import BaseScene


class Menu(BaseScene):
    """Main menu scene handling game option selection and rendering."""
    def __init__(self, screen: pygame.Surface) -> None:
        """Initialize the main menu with a set of selectable options and a uniform font style."""
        super().__init__(screen)
        self.index = 0
        self.options = ["Start", "Highscores", "Instructions", "Exit"]
        self.font = pygame.font.Font(None, 180)

    def handle_events(
        self, events: List[pygame.event.Event]
    ) -> Optional[Tuple[str, int]]:
        """Process keyboard navigation inputs to cycle or confirm menu options."""
        for event in events:
            if event.type == pygame.QUIT:
                return ("QUIT", 0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.index = (self.index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.index = (self.index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.select_options()
        return None

    def draw(self, screen: pygame.Surface) -> None:
        """Render the title header and dynamically scale the menu option elements."""
        screen.fill((0, 0, 0))
        sw, sh = screen.get_size()
        center_x = sw // 2
        title_surf = self.font.render("PAC-MAN", True, (255, 255, 0))
        t_scale = (sh * 0.12) / title_surf.get_height()
        title_surf = pygame.transform.scale_by(title_surf, t_scale)
        title_rect = title_surf.get_rect(center=(center_x, sh * 0.15))
        screen.blit(title_surf, title_rect)
        menu_base_y = sh * 0.40
        menu_spacing = sh * 0.10
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.index else (255, 255, 255)
            surf = self.font.render(option, True, color)
            if surf.get_height() > sh * 0.08:
                opt_scale = (sh * 0.08) / surf.get_height()
                surf = pygame.transform.scale_by(surf, opt_scale)
            screen.blit(
                surf, surf.get_rect(center=(center_x, menu_base_y + i * menu_spacing))
            )

    def select_options(self) -> Tuple[str, int]:
        """Map the currently highlighted menu option index to its designated state machine token."""
        option = self.options[self.index]
        if option == "Start":
            return ("GAME", 0)
        if option == "Highscores":
            return ("HIGHSCORES", 0)
        if option == "Instructions":
            return ("INSTRUCTIONS", 0)
        return ("QUIT", 0)
