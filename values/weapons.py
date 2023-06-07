import pygame

from weapons_classes import Sword, Bow, Shield
from values.sprite_groups import enemy_group, tiles_group, player_group

player_weapons = {"sword": Sword(30, 2, 0.2, enemy_group, 10, 10, 110),
                  "bow": Bow(25, 2, 0.2, enemy_group, tiles_group, 50, 500),
                  "shield": Shield(2)
                  }
enemy_weapons = {"sword": Sword(10, 2, 0.5, player_group, 8),
                 "bow": Bow(15, 1.5, 0.4, player_group, tiles_group, 8)}
