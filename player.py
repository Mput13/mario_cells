from basic_classes.basic_classes_for_live_object import LiveObject
from values.constants import RIGHT, LEFT, GRAVITY
from values.sprite_groups import all_sprites, player_group
from utils import alive_only
import pygame


class Player(LiveObject):
    IMAGE = pygame.image.load("data/animations/characters/player/mario.png")

    def __init__(self, pos, health, speed, tiles_group, direction=RIGHT):
        super().__init__(pos, health, speed, tiles_group, direction, player_group, all_sprites)
        self.image = Player.IMAGE
        self.rect = self.image.get_rect()
        self.weapon_1 = None
        self.weapon_2 = None

    def switch_weapons(self):
        self.weapon_1, self.weapon_2 = self.weapon_2, self.weapon_1

    def set_weapon_1(self, weapon):
        self.weapon_1 = weapon

    def set_weapon_2(self, weapon):
        self.weapon_2 = weapon


