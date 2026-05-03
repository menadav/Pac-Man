from src.engine.scene import BaseScene

class Menu(BaseScene):
    def __init__(self, screen: pygame.Surface) -> None:
        super.__()__(screen)
        self.options = ["Start", "Exit"]
        self.last_p = last_players
