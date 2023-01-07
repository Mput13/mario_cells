import collections

import pygame

from camera import Camera
from values.constants import WIDTH, HEIGHT, FPS
from level_work import generate_level, load_level
from values.sprite_groups import all_sprites, tiles_group
from utils import load_image


class Game:
    def __init__(self):
        self.running = False
        self.background = load_image("background.png")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.event_handlers = collections.defaultdict(list)
        self.player = None

    def setup(self):
        pass

    def register_event(self, event_type, action):
        self.event_handlers[event_type].append(action)

    def start(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        camera = Camera()
        self.player = generate_level(load_level('maps/test_level.txt'))
        self.running = True
        timer = pygame.time.Clock()
        self.running = True
        while self.running:
            key = pygame.key.get_pressed()
            delta_t = timer.tick(FPS) / 1000
            if key[pygame.K_a]:
                self.player.move(delta_t, left=True)
            if key[pygame.K_d]:
                self.player.move(delta_t, right=True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if callbacks := self.event_handlers[event.type]:
                    for callback in callbacks:
                        callback(event)
            screen.blit(self.background, (0, 0))
            all_sprites.draw(screen)
            self.update(screen, delta_t)
            pygame.display.flip()

    def update(self, surface, delta_t):
        if not pygame.sprite.spritecollideany(self.player, tiles_group):
            self.player.move(delta_t, down=True)


game = Game()
game.start()
