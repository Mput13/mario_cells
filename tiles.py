import pygame

from values.constants import WIDTH, HEIGHT, GRAVITY, TILE_SIZE
from values.sprite_groups import all_sprites, boxes_group, tiles_group, player_group
from utils import load_image

screen = pygame.display.set_mode((WIDTH, HEIGHT))
tile_images = {'block': load_image('data/world/block.png'), 'question_block': load_image('data/world/question_block.png'),
               'brick': load_image('data/world/brick.png'),
               'door': load_image('data/world/door.png'), 'hollow': load_image('data/world/hollow.png')}
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





