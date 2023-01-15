from basic_classes.for_collision import _Multiple
from utils import alive_only
from basic_classes.for_animation import ActionAnimatedSprite
from values.constants import GRAVITY, MAX_GRAVITY_SPEED
import pygame


class LiveObject(ActionAnimatedSprite):
    def __init__(self, pos: (int, int), actions, start_action_name, health, speed, tiles_group, direction, *groups):
        super().__init__(pos, actions, start_action_name, *groups)
        self.health = health
        self.speed = speed
        self.tiles_group = tiles_group
        self.direction = direction
        self.y_speed = 0
        self.x_speed = 0
        self.is_dead = False
        self.directions_movement = self.selection_possible_directions_movement()

    def selection_possible_directions_movement(self):
        collide = pygame.sprite.spritecollide(self, self.tiles_group, False)
        top = []
        left = []
        bottom = []
        right = []
        if collide:
            sides = ["top", "left", "bottom", "right"]
            check = _Multiple(sides)
            for element in collide:
                collisions = check.check_sides(self, element)
                top.append(collisions[sides[0]])
                left.append(collisions[sides[1]])
                bottom.append(collisions[sides[2]])
                right.append(collisions[sides[3]])
        directions_movement = {"left": not any(left),
                               "right": not any(right),
                               "bottom": not any(bottom),
                               "top": not any(top)}
        return directions_movement

    @alive_only
    def gravity(self, delta_t):
        if self.directions_movement["bottom"]:
            if self.y_speed < MAX_GRAVITY_SPEED:
                self.y_speed += delta_t * GRAVITY
        elif not self.directions_movement["bottom"]:
            self.y_speed = self.y_speed - self.y_speed
