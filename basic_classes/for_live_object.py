from basic_classes.for_collision import CollisionsEdges
from utils import alive_only
from basic_classes.for_animation import ActionAnimatedSprite
from values.constants import GRAVITY, MAX_GRAVITY_SPEED, WIDTH, HEIGHT
from typing import Any
from values.sprite_groups import all_sprites, enemy_group
import pygame


# Базовый класс с коллизией
# коллизия просчитывается автоматически в дочерних классах нужно только переопределить метод move
# если нужно добавить логику в update() можно использовать super()
# или переопределить update но тогда добавить логику коллизий
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
        self.creating_edges()
        self.collision_directions = None

    def creating_edges(self):
        creator_edges = CollisionsEdges((self.rect.x, self.rect.y), self.rect.height, self.rect.width)
        edges = creator_edges.creating_all_edges()
        self.top_edge = edges["top"]
        self.left_edge = edges["left"]
        self.right_edge = edges["right"]
        self.bottom_edge = edges["bottom"]

    def gravity(self, delta_t):
        if self.collision_directions["bottom"] and self.y_speed > 0:
            self.rect.move_ip(0, -self.y_speed * delta_t)
            self.move_edges(0, -self.y_speed * delta_t)
            self.y_speed = 0
        else:
            if self.y_speed < MAX_GRAVITY_SPEED:
                self.y_speed += delta_t * GRAVITY

    def dead(self):
        if self.health <= 0:
            self.is_dead = True

    def move_edges(self, x, y):
        self.top_edge.rect.move_ip(x, y)
        self.left_edge.rect.move_ip(x, y)
        self.bottom_edge.rect.move_ip(x, y)
        self.right_edge.rect.move_ip(x, y)

    def get_collision_directions(self):
        directions = {}
        if pygame.sprite.spritecollide(self.top_edge, self.tiles_group, False):
            directions["top"] = True
        else:
            directions["top"] = False
        if pygame.sprite.spritecollide(self.left_edge, self.tiles_group, False):
            directions["left"] = True
        else:
            directions["left"] = False
        if pygame.sprite.spritecollide(self.bottom_edge, self.tiles_group, False):
            directions["bottom"] = True
        else:
            directions["bottom"] = False
        if pygame.sprite.spritecollide(self.right_edge, self.tiles_group, False):
            directions["right"] = True
        else:
            directions["right"] = False
        self.collision_directions = directions

    def move(self):
        pass

    def collision_with_world(self):
        self.get_collision_directions()
        if self.collision_directions["top"] and self.y_speed < 0:
            self.y_speed = 0
        if self.collision_directions["left"] and self.x_speed < 0:
            self.rect.move_ip(-self.x_speed, 0)
            self.move_edges(-self.x_speed, 0)
        if self.collision_directions["right"] and self.x_speed > 0:
            self.rect.move_ip(-self.x_speed, 0)
            self.move_edges(-self.x_speed, 0)

    def update(self, delta_t, *args: Any, **kwargs: Any) -> None:
        super().update()
        self.collision_with_world()
        self.gravity(delta_t)
        self.move()
        self.move_edges(self.x_speed, self.y_speed)


class Enemy(LiveObject):
    def __init__(self, pos, actions, start_action_name, health, speed, weapon, tiles_group, direction):
        super().__init__(pos, actions, start_action_name, health, speed, tiles_group, direction, enemy_group,
                         all_sprites)
        self.weapon = weapon

    def creating_field_of_view(self):
        top = pygame.sprite.Sprite()
        top.rect = pygame.Rect(self.rect.center[0], self.rect.center[1] - HEIGHT // 2, 1, HEIGHT // 2)
