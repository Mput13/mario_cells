import random
import pygame
from pygame.sprite import AbstractGroup
from basic_classes.basic_classes_for_animation import ActionAnimation
from values.constants import GRAVITY, RIGHT, LEFT
from values.sprite_groups import all_sprites, active_weapons_group
from values.animation import BowAnimations
from typing import Any


class DealingDamage(pygame.sprite.Sprite):
    def __init__(self,
                 damage: int,
                 crit_multiplier: float,
                 crit_chance: float,
                 pos: (int, int),
                 enemy_group: AbstractGroup,
                 direction: int = 1,
                 *groups: AbstractGroup):
        super().__init__(*groups)

        self.damage = damage
        self.crit_multiplier = crit_multiplier
        self.crit_chance = crit_chance
        self.crit_damage = damage * crit_multiplier
        self.pos = pos
        self.direction = direction
        self.enemy_group = enemy_group

    def get_damage(self):
        number = random.random()
        if number <= self.crit_chance:
            return self.crit_damage
        return self.damage


class Sword(DealingDamage):
    IMAGE = pygame.image.load("data/sword1.png")

    def __init__(self,
                 damage: int,
                 crit_multiplier: float,
                 crit_chance: float,
                 pos: (int, int),
                 enemy_group: AbstractGroup,
                 speed: float = 1,
                 direction: int = 1):
        super().__init__(damage, crit_multiplier, crit_chance, pos, enemy_group, direction,
                         active_weapons_group, all_sprites)
        self.enemy_group = enemy_group
        self.original_image = Sword.IMAGE
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.radius = self.image.get_rect().height // 2
        self.angle = 10
        self.pos = pos
        self.angle = 10
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)
        self.conflict_list = []

    def update(self, *args: Any, **kwargs: Any) -> None:
        center = pygame.math.Vector2(self.pos) + pygame.math.Vector2(0, -self.radius).rotate(
            self.angle * self.direction)
        self.image = pygame.transform.rotate(self.original_image, -self.angle * self.direction)
        self.rect = self.image.get_rect(center=(round(center.x), round(center.y)))
        self.dealing_damage()
        self.turn_right()
        self.stop_animation()

    def turn_right(self):
        self.angle = self.angle + self.speed

    def stop_animation(self):
        if self.angle >= 90:
            self.kill()
            self.angle = 10

    def dealing_damage(self):
        collide = pygame.sprite.spritecollide(self, self.enemy_group, False, pygame.sprite.collide_mask)
        for enemy in collide:
            if enemy not in self.conflict_list:
                self.conflict_list.append(enemy)
                enemy.health -= self.get_damage()


class Arrow(DealingDamage):
    IMAGE_RIGHT = pygame.image.load("data/arrow_right.png")
    IMAGE_LEFT = pygame.image.load("data/arrow_left.png")

    def __init__(self,
                 damage: int,
                 crit_multiplier: float,
                 crit_chance: float,
                 pos: (int, int),
                 enemy_group: AbstractGroup,
                 tiles_group: AbstractGroup,
                 flight_speed: float = 1,
                 flight_range: int = 500,
                 direction: int = 1):
        super().__init__(damage, crit_multiplier, crit_chance, pos, enemy_group, direction, all_sprites)
        self.tiles_group = tiles_group
        self.selection_image()
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.flight_speed = pygame.Vector2(flight_speed * self.direction, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.gravity_speed = 0
        self.flight_range = flight_range

    def selection_image(self):
        if self.direction == RIGHT:
            self.image = Arrow.IMAGE_RIGHT
        else:
            self.image = Arrow.IMAGE_LEFT

    def dealing_damage(self):
        collide = pygame.sprite.spritecollideany(self, self.enemy_group)
        if collide is not None:
            collide.health -= self.get_damage()
            self.kill()

    def collision_with_tiles(self):
        collide = pygame.sprite.spritecollide(self, self.tiles_group, False)
        if collide:
            self.kill()

    def enabling_gravity(self, delta_t):
        start_x = self.pos[0]
        x = self.rect.center[0] - (self.rect.width // 2)
        if abs(start_x - x) >= self.flight_range:
            self.gravity_speed += delta_t * GRAVITY

    def update(self, delta_t, *args: Any, **kwargs: Any) -> None:
        self.enabling_gravity(delta_t)
        self.dealing_damage()
        self.collision_with_tiles()
        vector = self.flight_speed + pygame.Vector2(0, self.gravity_speed)
        self.rect.move_ip(*vector)


class Bow(DealingDamage):
    def __init__(self,
                 damage: int,
                 crit_multiplier: float,
                 crit_chance: float,
                 pos: (int, int),
                 enemy_group: AbstractGroup,
                 tiles_group: AbstractGroup,
                 flight_speed: float = 1,
                 flight_range: int = 500,
                 direction: int = 1):
        super().__init__(damage, crit_multiplier, crit_chance, pos, enemy_group, direction,
                         active_weapons_group, all_sprites)
        self.tiles_group = tiles_group
        self.flight_speed = flight_speed
        self.flight_range = flight_range
        self.choosing_direction()
        self.animation.set_play_single()
        self.image = self.animation.image
        self.rect = self.animation.rect
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.arrow_fired = False

    def choosing_direction(self):
        animations: dict[BowAnimations, BowAnimations] = {animation.name: animation.value for animation in
                                                          BowAnimations}
        if self.direction == RIGHT:
            self.animation: ActionAnimation = animations['shot_right']
        else:
            self.animation: ActionAnimation = animations['shot_left']

    def arrow_release(self):
        if self.animation.cur_frame == 12 and not self.arrow_fired:
            pos = (self.pos[0],
                   self.pos[1] + self.rect.height // 2 - Arrow.IMAGE_RIGHT.get_height() // 2)
            arrow = Arrow(self.damage, self.crit_multiplier, self.crit_chance, pos, self.enemy_group, self.tiles_group,
                          self.flight_speed, self.flight_range, self.direction)
            self.arrow_fired = True

    def stop_animation(self):
        if self.animation.cur_frame == 23:
            self.kill()
            self.animation.reset()

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.animation.update()
        self.arrow_release()
        self.image = self.animation.image
        self.stop_animation()


class Shield(pygame.sprite.Sprite):
    IMAGE_RIGHT = pygame.image.load("data/shield_right.png")
    IMAGE_LEFT = pygame.image.load("data/shield_left.png")

    def __init__(self,
                 pos: (int, int),
                 enemy_shells: AbstractGroup,
                 button,
                 direction: int = 1):
        super().__init__(all_sprites, active_weapons_group)
        self.direction = direction
        self.selection_image()
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.enemy_shells = enemy_shells
        self.button = button

    def selection_image(self):
        if self.direction == RIGHT:
            self.image = Shield.IMAGE_RIGHT
        else:
            self.image = Shield.IMAGE_LEFT

    #    def projectile_reflection(self):
    #        collide = pygame.sprite.spritecollide(self, self.enemy_shells, False)
    #        if collide:
    #            for shell in collide:
    #                speed = shell.flight_vector.x
    #                shell.flight_vector = pygame.Vector2(-speed, 0)

    def blocking(self):
        pass

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.blocking()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == self.button:
                self.kill()


pygame.init()
window = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()
sword = pygame.sprite.Group()
wall = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy_shells = pygame.sprite.Group()
run = True
shield_l = False
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not active_weapons_group:
                shield_l = Shield((340, 550), enemy_shells, event.button, LEFT)
                s_r = Shield((360, 550), enemy_shells, event.button, RIGHT)
                sw_l = Sword(1, 1, 1, (350, 150), enemy_group, 1, LEFT)
                sw_r = Sword(1, 1, 1, (350, 150), enemy_group, 1, RIGHT)
                b_r = Bow(1, 1, 1, (400, 350), enemy_group, wall, 2, 100, RIGHT)
                b_l = Bow(1, 1, 1, (300, 350), enemy_group, wall, 2, 100, LEFT)

        if event.type == pygame.QUIT:
            run = False
    delta_t = clock.tick(60) / 1000
    window.fill(0)
    all_sprites.update(delta_t=delta_t)

    window.fill(0)
    all_sprites.draw(window)
    pygame.display.flip()

pygame.quit()
exit()
