import collections

import pygame
import sys
import os

FPS = 50
WIDTH = 400
HEIGHT = 300

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


class Game:
    def __init__(self, width: int, height: int, fps: int = 0):
        self.height = height
        self.width = width
        self.fps = fps
        self.player = Player()
        self.enemis = None
        self.running = False
        self.background = pygame.Color('black')

        self.event_handlers = collections.defaultdict(list)

    def setup(self):
        pass

    def register_event(self, event_type, action):
        self.event_handlers[event_type].append(action)

    def start(self):
        screen = pygame.display.set_mode((self.width, self.height))

        timer = pygame.time.Clock()

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if callbacks := self.event_handlers[event.type]:
                    for callback in callbacks:
                        callback(event)

            screen.fill(self.background)
            delta_t = timer.tick(self.fps) / 1000
            self.update(screen, delta_t)
            pygame.display.flip()

    def update(self, surface, delta_t):
        pass


class Weapon:
    def __init__(self, damage, range):
        self.damage = damage
        self.range = range

    def shoot(self):
        pass


class Character(pygame.sprite.Sprite):
    image = load_image("characters/mario.png")

    def __init__(self, *group, speed=200, health=100):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. Это очень важно !!!
        super().__init__(*group)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.health = health

    def move(self):
        pass


class Player(Character):
    def bow_shot(self):
        pass

    def blade_shot(self):
        pass

    def shild_shot(self):
        pass

    def move(self):
        pass


class Texture(pygame.sprite.Sprite):
    image = load_image("textures/mario.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. Это очень важно !!!
        super().__init__(*group)
        self.image = Texture.image


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.delimeter = 10

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx // self.delimeter
        obj.rect.y += self.dy // self.delimeter

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


characters = pygame.sprite.Group()
Character(*characters)
textures = pygame.sprite.Group()
Texture(*textures)
