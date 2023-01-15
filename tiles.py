import pygame

from values.constants import WIDTH, HEIGHT, GRAVITY, JUMP_SPEED
from values.sprite_groups import all_sprites, boxes_group, tiles_group
from values.constants import SIZE_BLOCK
from utils import load_image

screen = pygame.display.set_mode((WIDTH, HEIGHT))
tile_images = {'block': load_image('world/block.png'), 'question_block': load_image('world/question_block.png'),
               'brick': load_image('world/brick.png')}
tile_width = tile_height = SIZE_BLOCK


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





