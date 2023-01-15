from basic_classes.for_live_object import LiveObject
from values.constants import RIGHT, LEFT, GRAVITY, JUMP_SPEED
from values.sprite_groups import all_sprites, player_group
from values.animations import PlayerAnimations
from weapons_classes import Sword, Bow, Shield
from utils import alive_only
from typing import Any
import pygame


class Player(LiveObject):

    def __init__(self, pos, health, speed, tiles_group, enemy_group, weapon_1, weapon_2, direction=RIGHT):
        self.animations: dict[PlayerAnimations, PlayerAnimations] = {
            animation.name: animation.value for animation in PlayerAnimations
        }
        super().__init__(pos, self.animations, PlayerAnimations.idle_right.name, health, speed, tiles_group, direction,
                         player_group, all_sprites)
        self.weapon_1 = weapon_1
        self.weapon_2 = weapon_2
        self.enemy_group = enemy_group
        self.active_weapon = pygame.sprite.Group()

    def switch_weapons(self):
        self.weapon_1, self.weapon_2 = self.weapon_2, self.weapon_1

    def set_weapon_1(self, weapon):
        self.weapon_1 = weapon

    def set_weapon_2(self, weapon):
        self.weapon_2 = weapon

    @alive_only
    def start_move(self, event):
        if event.key == pygame.K_a:
            self.x_speed = -self.speed
            self.flip_left()
            self.direction = LEFT
        elif event.key == pygame.K_d:
            self.x_speed = self.speed
            self.flip_right()
            self.direction = RIGHT
        if event.key in (pygame.K_d, pygame.K_a) and not self.directions_movement["bottom"]:
            self.switch_undirected("walk")

    @alive_only
    def stop_move(self, event):
        if event.key in (pygame.K_a, pygame.K_d):
            #            if pygame.key.get_pressed()[pygame.K_a]:
            #                self.x_speed =
            self.x_speed = 0
            if not self.directions_movement["bottom"]:
                self.switch_undirected("idle")

    @alive_only
    def use_weapon(self, event):
        #        if not self.directions_movement["bottom"]:
        if not self.active_weapon:
            button = event.button
            if button in (pygame.BUTTON_RIGHT, pygame.BUTTON_LEFT):
                if self.direction == RIGHT:
                    coefficient = self.rect.width
                else:
                    coefficient = 0
                pos = (self.rect.x + coefficient, self.rect.y - self.rect.height // 4)
                if button == pygame.BUTTON_LEFT:
                    self.weapon_1.attack(pos, self.direction, self.active_weapon)
                elif button == pygame.BUTTON_RIGHT:
                    self.weapon_2.attack(pos, self.direction, self.active_weapon)

    @alive_only
    def jump(self, event):
        if event.key in (pygame.K_SPACE, pygame.K_w) and not self.directions_movement["bottom"]:
            self.y_speed = JUMP_SPEED
            self.switch_undirected("jump")

    @alive_only
    def move(self, delta_t):
        self.gravity(delta_t)
        if self.active_weapon:
            self.x_speed = 0
        if self.x_speed > 0 and not self.directions_movement["right"]:
            self.x_speed = 0
        elif self.x_speed < 0 and not self.directions_movement["left"]:
            self.x_speed = 0
        if self.x_speed < 0 and not self.directions_movement["top"]:
            self.y_speed = 0

        if self.directions_movement["bottom"]:
            self.switch_undirected("jump")
        self.rect.move_ip(self.x_speed, self.y_speed)

    def update(self, delta_t, *args: Any, **kwargs: Any) -> None:
        super().update()
        self.selection_possible_directions_movement()
        self.move(delta_t)
