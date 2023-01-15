import collections

import pygame

from camera import Camera
from values.constants import GRAVITY, WIDTH, HEIGHT, FPS
from level_work import generate_level, load_level
from values.sprite_groups import all_sprites, tiles_group, boxes_group
from utils import load_image


class Game:
    def __init__(self):
        self.running = False
        self.background = load_image("world/background.png")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.event_handlers = collections.defaultdict(list)
        self.player = None
        self.is_jump = False

    def setup(self):
        pass

    def register_event(self, event_type, action):
        self.event_handlers[event_type].append(action)

    def start(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        camera = Camera()
        self.player = generate_level(load_level('test_level.txt'))
        self.running = True
        print(tiles_group.sprites())
        timer = pygame.time.Clock()
        self.running = True
        self.register_event(pygame.KEYDOWN, self.player.start_move)
        self.register_event(pygame.KEYUP, self.player.stop_move)
        self.register_event(pygame.KEYDOWN, self.player.jump)
        self.register_event(pygame.MOUSEBUTTONDOWN, self.player.use_weapon)
        while self.running:
            delta_t = timer.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if callbacks := self.event_handlers[event.type]:
                    for callback in callbacks:
                        callback(event)
            screen.blit(self.background, (0, 0))
            all_sprites.draw(screen)
            self.update(screen, delta_t, event)
            pygame.display.flip()

    def update(self, surface, delta_t, event):
        all_sprites.update(delta_t, event)


game = Game()
game.start()
