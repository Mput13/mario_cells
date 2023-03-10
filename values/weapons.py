import pygame

from weapons_classes import Sword, Bow, Shield
from values.sprite_groups import enemy_group, tiles_group, player_group

player_weapons = {"sword": Sword(20, 2, 0.2, enemy_group, 10, 10, 110),
                  "bow": Bow(10, 2, 0.2, enemy_group, tiles_group, 50, 500),
                  "shield_right_click": Shield(pygame.BUTTON_RIGHT),
                  "shield_left_click": Shield(pygame.BUTTON_LEFT)
                  }
enemy_weapons = {"sword": Sword(10, 2, 0.5, player_group, 8),
                 "bow": Bow(15, 1.5, 0.4, player_group, tiles_group, 8)}
