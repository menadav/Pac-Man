import pygame
from typing import List, Optional
from src.engine.scene import BaseScene

class Instructions(BaseScene):
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font = pygame.font.Font(None, 100)
        self.options = ["Return"]

    def handle_events(
            self, events: List[str]
            ) -> Optional[str]:
        for event in events:
             if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return self.select_options()
        return None

    def draw(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))
        sw, sh = screen.get_size()
        center_x = sw // 2
        title_surf = self.font.render("INSTRUCTIONS", True, (255, 255, 0))
        t_scale = (sh * 0.12) / title_surf.get_height()
        title_surf = pygame.transform.scale_by(title_surf, t_scale)
        screen.blit(title_surf, title_surf.get_rect(center=(center_x, sh * 0.15)))

        # 2. CUERPO DE TEXTO (Instrucciones)
        # Definimos las líneas de texto
        instructions_text = [
            "Use ARROW KEYS to move Pac-Man",
            "Eat all the dots to win",
            "Avoid the GHOSTS!",
            "Power Pellets let you eat ghosts",
            "",
            "Press ENTER to Return",
        ]
        start_y = sh * 0.40
        line_spacing = sh * 0.08
        for i, line in enumerate(instructions_text):
            color = (255, 255, 0) if "Return" in line else (255, 255, 255)
            surf = self.font.render(line, True, color)
            content_scale = (sh * 0.06) / surf.get_height()
            surf = pygame.transform.scale_by(surf, content_scale)
            if surf.get_width() > sw * 0.9:
                surf = pygame.transform.scale(surf, (int(sw * 0.9), int(surf.get_height())))
            screen.blit(surf, surf.get_rect(center=(center_x, start_y + i * line_spacing)))

    def select_options(self):
        option = self.options[0]
        if option == "Return":
            return "MENU"