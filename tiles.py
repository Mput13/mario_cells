import pygame

from colisions import bottom
from values.constants import WIDTH, HEIGHT, GRAVITY, TILE_SIZE
from values.sprite_groups import all_sprites, boxes_group, tiles_group, player_group
from utils import load_image

screen = pygame.display.set_mode((WIDTH, HEIGHT))
tile_images = {'block': load_image('data/block.png'), 'question_block': load_image('data/question_block.png'),
               'brick': load_image('data/brick.png'), 'player': load_image('data/characters/mario.png'),
               'door': load_image('data/door.png')}
player_image = load_image('data/characters/mario.png')
tile_width = tile_height = TILE_SIZE


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *group):
        self.type = tile_type
        super().__init__(tiles_group, all_sprites, *group)
        self.image = tile_images[tile_type]
        if tile_type == 'door':
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y - TILE_SIZE)
        else:
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)


class QuestionBox(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(boxes_group, tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Character(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *group, speed=600, health=100):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. Это очень важно !!!
        super().__init__(all_sprites, player_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect()
        self.x_speed = speed
        self.y_speed = GRAVITY
        self.health = health


class Player(Character):
    def __init__(self, pos_x, pos_y, *group):
        tile_type = 'player'
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


class Door(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images['door']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
