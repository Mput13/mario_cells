import collections
from typing import Callable

import pygame


class Game:
    def __init__(self, width: int, height: int, screen, fps: int = 0):
        self.height = height
        self.width = width
        self.fps = fps

        self.running = False

        self.screen = screen

        self.event_handlers: dict[int, list[Callable[[pygame.event.Event], None]]] = collections.defaultdict(list)

    def setup(self):
        pass

    def register_event(self, event_type: int, action: Callable[[pygame.event.Event], None]):
        self.event_handlers[event_type].append(action)

    def start(self):

        timer = pygame.time.Clock()

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if callbacks := self.event_handlers[event.type]:
                    for callback in callbacks:
                        callback(event)
            delta_t = timer.tick(self.fps) / 1000
            self.screen.fill(pygame.Color('black'))
            self.draw(self.screen)
            self.update(delta_t)
            pygame.display.flip()

    def update(self, delta_t: float):
        pass

    def draw(self, screen: pygame.Surface):
        pass
