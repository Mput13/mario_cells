import collections

import pygame

from camera import Camera
from constants import GRAVITY, WIDTH, HEIGHT, FPS
from level_work import generate_level, load_level
from utils import load_image


class Game:
    def __init__(self):
        self.player = Player()
        self.running = False
        self.background = load_image("background.png")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.event_handlers = collections.defaultdict(list)

    def setup(self):
        pass

    def register_event(self, event_type, action):
        self.event_handlers[event_type].append(action)

    def start(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        camera = Camera()
        player, level_x, level_y = generate_level(load_level('test_level.txt'))
        self.running = True
        timer = pygame.time.Clock()
        self.running = True

        while self.running:
            delta_t = timer.tick(FPS) / 1000
            key = pygame.key.get_pressed()
            if key[pygame.K_a]:
                player.move(delta_t, left=True)
            elif key[pygame.K_d]:
                player.move(delta_t)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if callbacks := self.event_handlers[event.type]:
                    for callback in callbacks:
                        callback(event)
            screen.blit(self.background, (0, 0))
            self.update(screen, delta_t)
            pygame.display.flip()

    def update(self, surface, delta_t):
        pass


class Character(pygame.sprite.Sprite):
    def __init__(self, *group, speed=200, health=100):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. Это очень важно !!!
        super().__init__(*group)
        self.rect = self.image.get_rect()
        self.x_speed = speed
        self.y_speed = -GRAVITY
        self.health = health


class Player:
    def bow_shot(self):
        pass

    def blade_shot(self):
        pass

    def shild_shot(self):
        pass

    def move(self, delta_t, left=False, right=False):
        if right:
            self.rect.x += self.x_speed * delta_t
        elif left:
            self.rect.x -= self.x_speed * delta_t


game = Game()
game.start()
