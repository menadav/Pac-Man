import pygame
from typing import Optional, List
from abc import ABC, abstractmethod
from src.parse.models import ParseConfig


class BaseScene(ABC):
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

    @abstractmethod
    def handle_events(self, events: List[pygame.event.Event]) -> Optional[str]:
        pass

    @abstractmethod
    def draw(self, scree: pygame.Surface) -> None:
        pass
