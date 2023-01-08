from tiles import Tile, Player
import os


def load_level(filename):
    fullname = os.path.join('maps', filename)
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
                player = Player(x, y)
    return player
