import collections

import pygame
import sys
import os

from camera import Camera
from constants import GRAVITY
from sprite_groups import tiles_group, all_sprites, boxes_group

from utils import generate_level, load_level, load_image


class Game:
    def __init__(self, width: int, height: int, fps: int = 0):
        self.height = height
        self.width = width
        self.fps = fps
        self.player = Player()
        self.enemis = None
        self.running = False
        self.background = pygame.Color('black')

        self.event_handlers = collections.defaultdict(list)

    def setup(self):
        self.register_event()

    def register_event(self, event_type, action):
        self.event_handlers[event_type].append(action)

    def start(self):
        screen = pygame.display.set_mode((self.width, self.height))
        camera = Camera()
        player, level_x, level_y = generate_level(load_level(''))

        running = True
        timer = pygame.time.Clock()
        self.running = True
        while self.running:
            delta_t = timer.tick(self.fps) / 1000
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

            screen.fill(self.background)
            self.update(screen, delta_t)
            pygame.display.flip()

    def update(self, surface, delta_t):
        pass


class QuestionBox(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(boxes_group, tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Character(pygame.sprite.Sprite):
    image = load_image("characters/mario.png")

    def __init__(self, *group, speed=200, health=100):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. Это очень важно !!!
        super().__init__(*group)
        self.rect = self.image.get_rect()
        self.x_speed = speed
        self.y_speed = -GRAVITY
        self.health = health


class Player(Character):
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


tile_images = {'block': 'block.png', 'qustion_block': 'qustion_block.png'}
player_image = load_image('characters/mario.png')
tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
