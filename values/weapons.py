import pygame

from weapons_classes import Sword, Bow, Shield
from values.sprite_groups import enemy_group, tiles_group

player_weapons = {"sword": Sword(1, 1, 1, enemy_group, 1, 10),
                  "bow": Bow(1, 1, 1, enemy_group, tiles_group, 1, 500),
                  "shield_right_click": Shield(pygame.BUTTON_RIGHT),
                  "shield_left_click": Shield(pygame.BUTTON_LEFT)
                  }
