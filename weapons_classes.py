import random
import pygame
from pygame.sprite import AbstractGroup
from basic_classes.for_animation import ActionAnimation
from values.constants import GRAVITY, RIGHT, LEFT
from values.sprite_groups import all_sprites
from values.animations import BowAnimations
from typing import Any


class DealingDamage(pygame.sprite.Sprite):
    def __init__(self,
                 damage: int,
                 crit_multiplier: float,
                 crit_chance: float,
                 enemy_group: AbstractGroup,
                 *groups: AbstractGroup):
        super().__init__(*groups)

        self.damage = damage
        self.crit_multiplier = crit_multiplier
        self.crit_chance = crit_chance
        self.crit_damage = damage * crit_multiplier
        self.enemy_group = enemy_group
        self.pos = None
        self.direction = None
        self.is_attacking = False

    def get_damage(self):
        number = random.random()
        if number <= self.crit_chance:
            return self.crit_damage
        return self.damage

    def attack(self, pos, direction, weapon_group: AbstractGroup):
        self.direction = direction
        self.pos = pos
        weapon_group.add(self)
        all_sprites.add(self)
        self.is_attacking = True


class Sword(DealingDamage):
    IMAGE = pygame.image.load("data/weapons/sword.png")

    def __init__(self,
                 damage: int,
                 crit_multiplier: float,
                 crit_chance: float,
                 enemy_group: AbstractGroup,
                 speed: float = 1,
                 start_angele=10,
                 *group):
        super().__init__(damage, crit_multiplier, crit_chance, enemy_group, *group)
        self.enemy_group = enemy_group
        self.original_image = Sword.IMAGE
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.radius = self.image.get_rect().height // 2
        self.start_angle = start_angele
        self.angle = start_angele
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)
        self.conflict_list = []

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.is_attacking:
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
            self.angle = self.start_angle
            self.conflict_list.clear()
            self.is_attacking = False

    def dealing_damage(self):
        collide = pygame.sprite.spritecollide(self, self.enemy_group, False, pygame.sprite.collide_mask)
        for enemy in collide:
            if enemy not in self.conflict_list:
                self.conflict_list.append(enemy)
                enemy.health -= self.get_damage()


class Arrow(DealingDamage):
    IMAGE_RIGHT = pygame.image.load("data/weapons/arrow_right.png")
    IMAGE_LEFT = pygame.image.load("data/weapons/arrow_left.png")

    def __init__(self,
                 damage: int,
                 crit_multiplier: float,
                 crit_chance: float,
                 pos: (int, int),
                 enemy_group: AbstractGroup,
                 tiles_group: AbstractGroup,
                 direction,
                 flight_speed: float = 1,
                 flight_range: int = 500):
        super().__init__(damage, crit_multiplier, crit_chance, enemy_group, all_sprites)
        self.tiles_group = tiles_group
        self.direction = direction
        self.selection_image()
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.x = pos[0]
        self.rect.y = pos[1]
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
                 enemy_group: AbstractGroup,
                 tiles_group: AbstractGroup,
                 flight_speed: float = 1,
                 flight_range: int = 500,
                 *group):
        super().__init__(damage, crit_multiplier, crit_chance, enemy_group, *group)
        self.tiles_group = tiles_group
        self.flight_speed = flight_speed
        self.flight_range = flight_range
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
                          self.direction, self.flight_speed, self.flight_range)
            self.arrow_fired = True

    def stop_animation(self):
        if self.animation.cur_frame == 23:
            self.kill()
            self.animation.reset()
            self.arrow_fired = False

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.is_attacking:
            self.animation.update()
            self.arrow_release()
            self.image = self.animation.image
            self.stop_animation()

    def attack(self, pos, direction, weapon_group: AbstractGroup):
        super().attack(pos, direction, weapon_group)
        self.choosing_direction()
        self.image = self.animation.image
        self.rect = self.animation.rect
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.animation.set_play_single()


class Shield(pygame.sprite.Sprite):
    IMAGE_RIGHT = pygame.image.load("data/weapons/shield_right.png")
    IMAGE_LEFT = pygame.image.load("data/weapons/shield_left.png")

    def __init__(self,
                 button,
                 *group):
        super().__init__(*group)
        self.direction = None
        self.button = button
        self.is_attacking = False

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

    def update(self, delt_t, event, *args: Any, **kwargs: Any) -> None:
        if self.is_attacking:
            self.blocking()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == self.button:
                    self.kill()
                    self.is_attacking = False

    def attack(self, pos, direction, weapon_group: AbstractGroup):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.direction = direction
        self.selection_image()
        self.rect = self.image.get_rect()
        weapon_group.add(self)
        all_sprites.add(self)
        self.is_attacking = True
