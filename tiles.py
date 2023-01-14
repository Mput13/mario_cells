import pygame

from values.constants import WIDTH, HEIGHT, GRAVITY, JUMP_SPEED
from values.sprite_groups import all_sprites, boxes_group, tiles_group
from utils import load_image

screen = pygame.display.set_mode((WIDTH, HEIGHT))
tile_images = {'block': load_image('block.png'), 'question_block': load_image('question_block.png'),
               'brick': load_image('brick.png'), 'player': load_image('characters/mario.png')}
player_image = load_image('characters/mario.png')
tile_width = tile_height = 60


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class QuestionBox(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(boxes_group, tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Character(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *group, speed=400, health=100):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect()
        self.x_speed = speed
        self.y_speed = GRAVITY
        self.health = health


class Player(Character):
    def __init__(self, pos_x, pos_y, *group):
        tile_type = 'player'
        self.jump_count = -10
        super().__init__(tile_type, pos_x, pos_y, *group)

    def bow_shot(self):
        pass

    def blade_shot(self):
        pass

    def shild_shot(self):
        pass

    def move(self, delta_t, left=False, right=False, down=False, up=False):
        if right:
            self.rect.x += self.x_speed * delta_t
        elif left:
            self.rect.x -= self.x_speed * delta_t
        elif down:
            self.rect.y -= self.y_speed * delta_t
        elif up and pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.y -= self.y_speed * delta_t
        else:
            self.rect.y += self.y_speed * delta_t
