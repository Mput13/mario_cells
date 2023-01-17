from tiles import Tile
from player import Player
from values.constants import SIZE_BLOCK
from values.sprite_groups import tiles_group, enemy_group, door_group
from values.weapons import player_weapons
import os


def load_level(filename):
    fullname = f'{os.getcwd()}\maps\{filename}'
    print(fullname)
    with open(fullname, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('block', x, y)
            elif level[y][x] == '.':
                Tile('brick', x, y)
            elif level[y][x] == '@':
                pos_player = (x * SIZE_BLOCK, y * SIZE_BLOCK)
            elif level[y][x] == 'D':
                Tile('door', x, y, door_group)
    return Player(pos_player, 1, 5, tiles_group, enemy_group, player_weapons["sword"], player_weapons["bow"])
