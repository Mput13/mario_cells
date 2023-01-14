from tiles import Tile, Player
from values.constants import WIDTH, HEIGHT, TILE_SIZE
from values.sprite_groups import door_group, player_group


def load_level(filename):
    filename = filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line for line in mapFile]
    return level_map


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('block', x, y)
            elif level[y][x] == '.':
                Tile('brick', x, y)
            elif level[y][x] == '@':
                player = Player(x, y, player_group)
            elif level[y][x] == 'D':
                Tile('door', x, y, door_group)
    return player
