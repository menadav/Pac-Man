import src.engine.env
try:
    import pygame
except ImportError:
    raise ValueError("[ERROR] Install Pygame")
from src.engine.menu import Menu
from src.parse.models import ParseConfig

class GameMannager:
    def __init__(self, data: ParseConfig) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((2600, 1600))
        self.data = data
        self.menu = Menu(self.screen)

    def run(self) -> None:
        play = True
        while play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
        pygame.display.flip()
        pygame.quit()

