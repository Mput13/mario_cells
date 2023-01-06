import random
from utils import load_image
import pygame
from pygame.sprite import AbstractGroup


class Weapon(pygame.sprite.Sprite):
    def __int__(self, damage: int,
                crit_multiplier: float,
                crit_chance: float,
                pos: [int, int],
                *group: AbstractGroup):
        super().__int__(*group)

        self.damage = damage
        self.crit_multiplier = crit_multiplier
        self.crit_chance = crit_chance
        self.crit_damage = damage * crit_multiplier
        self.pos = pos

    def get_damage(self):
        number = random.random()
        if number <= self.crit_chance:
            return self.crit_damage
        return self.damage


class Sword(Weapon):
    IMAGE = load_image("sword1.png")

    def __int__(self, damage: int,
                crit_multiplier: float,
                crit_chance: float,
                pos: [int, int],
                enemy_sprites: AbstractGroup,
                speed: float = 1):
        super().__int__(damage, crit_multiplier, crit_chance, pos, weapons_sprites, all_sprites)
        self.enemy_sprites = enemy_sprites
        self.weapons_sprites = weapons_sprites
        self.original_image = Sword.IMAGE
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.radius = self.image.get_rect().height // 2
        self.angle = 10
        self.pos = pos
        self.animate = False
        self.angle = 10
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)
        self.conflict_list = []

    def update(self):
        if self.animate:
            center = pygame.math.Vector2(self.pos) + pygame.math.Vector2(0, -self.radius).rotate(self.angle)
            self.image = pygame.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(center=(round(center.x), round(center.y)))
            self.dealing_damage()
            self.turn_right()
            self.stop_animation()

    def turn_right(self):
        self.angle = self.angle + self.speed

    def start_animation(self):
        self.animate = True

    def stop_animation(self):
        if self.angle >= 90:
            self.kill()
            self.animate = False
            self.angle = 10

    def dealing_damage(self):
        collide = pygame.sprite.spritecollide(self, self.enemy_sprites, False, pygame.sprite.collide_mask)
        for el in collide:
            if el not in self.conflict_list:
                self.conflict_list.append(el)
                el.health -= self.get_damage()


