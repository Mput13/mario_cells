from basic_classes_for_animation import ActionAnimatedSprite
from basic_classes_for_collision import _Multiple
from utils import alive_only
from values.constants import GRAVITY, MAX_GRAVITY_SPEED
import pygame


class LiveObject(ActionAnimatedSprite):
    def __init__(self, pos: (int, int), health, speed, tiles_group, direction, *groups):
        super().__init__(*groups)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.health = health
        self.speed = speed
        self.tiles_group = tiles_group
        self.direction = direction
        self.y_speed = None
        self.x_speed = None
        self.is_death = False
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

    def dead(self):
        if self.health <= 0:
            self.is_death = not self.is_death

    @alive_only
    def gravity(self, delta_t):
        if self.directions_movement["bottom"]:
            if self.y_speed < MAX_GRAVITY_SPEED:
                self.y_speed += delta_t * GRAVITY
        else:
            self.y_speed = 0

    @alive_only
    def move(self):
        pass

    def update(self, *args: Any, **kwargs: Any) -> None:
        super().update()
        self.dead()
        self.move()

