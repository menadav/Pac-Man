from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

import pygame


class BaseScene(ABC):
    """Abstract base class representing a generic scene or state within the game."""
    def __init__(self, screen: pygame.Surface) -> None:
        """Initialize the scene with a reference to the main display surface."""
        self.screen = screen

    @abstractmethod
    def handle_events(
        self, events: List[pygame.event.Event]
    ) -> Optional[Tuple[str, int]]:
        """Process input events and optionally return a scene signal and score."""
        ...

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Render the scene components onto the provided display surface."""
        ...
