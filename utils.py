import os
import sys
from typing import Callable, TypeVar

import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def get_files_in_directory(directory_name):
    output = []
    for root, dirs, files in os.walk(f'{os.getcwd()}\{directory_name}'):
        for filename in files:
            output.append(filename)
    return output


def get_path(file):
    return f'{os.getcwd()}\{file}'


Func = TypeVar('Func', bound=Callable)


def alive_only(func: Func) -> Func:
    def wrapper(self, *args, **kwargs):
        if self.is_dead:
            return
        return func(self, *args, **kwargs)

    return wrapper
