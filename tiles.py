import pygame

from constants import WIDTH, HEIGHT
from sprite_groups import all_sprites, boxes_group, tiles_group
from utils import load_image

screen = pygame.display.set_mode((WIDTH, HEIGHT))
tile_images = {'block': load_image('block.png'), 'question_block': load_image('question_block.png'),
               'brick': load_image('brick.png')}
player_image = load_image('characters/mario.png')
tile_width = tile_height = 50


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
