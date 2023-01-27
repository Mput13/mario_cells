from basic_classes.for_live_object_and_enemy import LiveObject
from sounds import jump_sound
from values.constants import RIGHT, LEFT, GRAVITY, JUMP_SPEED
from values.sprite_groups import all_sprites, player_group
from values.animations import PlayerAnimations
from weapons_classes import Sword, Bow, Shield
from utils import alive_only
from typing import Any
import pygame


class Player(LiveObject):

    def __init__(self, pos, health, speed, tiles_group, opponent_group, weapon_1, weapon_2, direction=RIGHT):
        self.animations: dict[PlayerAnimations, PlayerAnimations] = {
            animation.name: animation.value for animation in PlayerAnimations
        }
        super().__init__(pos, self.animations, PlayerAnimations.idle_right.name, health, speed, tiles_group,
                         opponent_group, direction, player_group, all_sprites)
        self.weapon_1 = weapon_1
        self.weapon_2 = weapon_2
        self.is_walking = False

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
        if event.key in (pygame.K_d, pygame.K_a):
            self.is_walking = True
            if self.collision_directions["bottom"]:
                self.switch_undirected("walk")

    @alive_only
    def stop_move(self, event):
        if event.key in (pygame.K_a, pygame.K_d):
            if pygame.key.get_pressed()[pygame.K_a]:
                self.x_speed = -self.speed
                self.flip_left()
                self.direction = LEFT
            elif pygame.key.get_pressed()[pygame.K_d]:
                self.x_speed = self.speed
                self.flip_right()
                self.direction = RIGHT
            else:
                self.x_speed = 0
                self.is_walking = False
                if self.collision_directions["bottom"]:
                    self.switch_undirected("idle")

    @alive_only
    def use_weapon(self, event):
        if self.collision_directions["bottom"]:
            if not self.active_weapon:
                button = event.button
                if button in (pygame.BUTTON_RIGHT, pygame.BUTTON_LEFT):
                    if self.direction == RIGHT:
                        coefficient = self.rect.width
                    else:
                        coefficient = 0
                    pos = (self.rect.x + coefficient, self.rect.y + self.rect.height // 2)
                    if button == pygame.BUTTON_LEFT:
                        self.weapon_1.attack(pos, self.direction, self.active_weapon)
                    elif button == pygame.BUTTON_RIGHT:
                        self.weapon_2.attack(pos, self.direction, self.active_weapon)

    @alive_only
    def jump(self, event):
        if not self.active_weapon:
            if event.key in (pygame.K_SPACE, pygame.K_w) and self.collision_directions["bottom"]:
                self.y_speed = JUMP_SPEED
                jump_sound.play()

    def move(self):
        if not self.collision_directions["bottom"]:
            self.switch_undirected("jump")
        if self.collision_directions["bottom"]:
            if self.is_walking:
                self.switch_undirected("walk")
            else:
                self.switch_undirected("idle")
        self.rect.move_ip(self.x_speed, self.y_speed)

    def update(self, delta_t, *args: Any, **kwargs: Any) -> None:
        if self.active_weapon:
            self.switch_undirected("idle")
        super().update(delta_t)
