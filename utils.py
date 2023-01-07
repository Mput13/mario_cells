import os
import sys
from  typing import Callable, TypeVar

import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


Func = TypeVar('Func', bound=Callable)


def alive_only(func: Func) -> Func:
    def wrapper(self, *args, **kwargs):
        if self.is_dead:
            return
        return func(self, *args, **kwargs)

    return wrapper
