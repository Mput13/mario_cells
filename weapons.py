import random
from utils import load_image
import pygame
from pygame.sprite import AbstractGroup
from basic_classes.basic_classes_for_animation import ActionAnimatedSprite
from constants import GRAVITY
from sprite_groups import all_sprites, active_weapons_group
from typing import Any


class Weapon(pygame.sprite.Sprite):
    def __init__(self,
                 damage: int,
                 crit_multiplier: float,
                 crit_chance: float,
                 pos: (int, int),
                 enemy_group: AbstractGroup,
                 *groups: AbstractGroup):
        super().__init__(*groups)

        self.damage = damage
        self.crit_multiplier = crit_multiplier
        self.crit_chance = crit_chance
        self.crit_damage = damage * crit_multiplier
        self.pos = pos
        self.is_right_rotated = 1
        self.enemy_group = enemy_group

    def change_direction(self):
        self.is_right_rotated *= -1

    def get_damage(self):
        number = random.random()
        if number <= self.crit_chance:
            return self.crit_damage
        return self.damage


class Sword(Weapon):
    IMAGE = pygame.image.load("data/sword1.png")

    def __init__(self,
                 damage: int,
                 crit_multiplier: float,
                 crit_chance: float,
                 pos: (int, int),
                 enemy_group: AbstractGroup,
                 speed: float = 1):
        super().__init__(damage, crit_multiplier, crit_chance, pos, enemy_group,
                         active_weapons_group, all_sprites)
        self.enemy_group = enemy_group
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

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.animate:
            center = pygame.math.Vector2(self.pos) + pygame.math.Vector2(0, -self.radius).rotate(
                self.angle * self.is_right_rotated)
            self.image = pygame.transform.rotate(self.original_image, -self.angle * self.is_right_rotated)
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
        collide = pygame.sprite.spritecollide(self, self.enemy_group, False, pygame.sprite.collide_mask)
        for enemy in collide:
            if enemy not in self.conflict_list:
                self.conflict_list.append(enemy)
                print(2)


#                enemy.health -= self.get_damage()


class Bow(ActionAnimatedSprite):
    pass


class Arrow(Weapon):
    IMAGE = pygame.image.load("data/arrow.png")

    def __init__(self,
                 damage: int,
                 crit_multiplier: float,
                 crit_chance: float,
                 pos: (int, int),
                 enemy_group: AbstractGroup,
                 tiles_group: AbstractGroup,
                 speed: float = 1,
                 flight_range: int = 500):
        super().__init__(damage, crit_multiplier, crit_chance, pos, enemy_group, all_sprites)
        self.tiles_group = tiles_group
        self.original_image = Arrow.IMAGE
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.pos = pos
        self.flight_vector = pygame.Vector2(speed, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.gravity_speed = 0
        self.flight_range = flight_range

    def dealing_damage(self):
        collide = pygame.sprite.spritecollideany(self, self.enemy_group, pygame.sprite.collide_mask)
        if collide is not None:
            collide.health -= self.get_damage()
            self.kill()

    def collision_with_tiles(self):
        collide = pygame.sprite.spritecollide(self, self.tiles_group, False, pygame.sprite.collide_mask)
        if collide:
            self.kill()

    def enabling_gravity(self, delta_t):
        start_x = self.pos[0]
        x = self.rect.center[0]
        if abs(start_x - x) >= self.flight_range:
            self.gravity_speed += delta_t * 4

    def update(self, delta_t, *args: Any, **kwargs: Any) -> None:
        self.enabling_gravity(delta_t)
        self.dealing_damage()
        self.collision_with_tiles()
        vector = self.flight_vector * self.is_right_rotated + pygame.Vector2(0, self.gravity_speed)
        self.rect.move_ip(*vector)
