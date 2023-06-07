from basic_classes.for_collision_and_enemy_AI import CollisionsEdges, FieldViewEnemy, SearchVoid, AttackField
from utils import alive_only
from basic_classes.for_animation import ActionAnimatedSprite, ActionAnimation
from values.constants import GRAVITY, MAX_GRAVITY_SPEED, RIGHT, LEFT, JUMP_SPEED
from values.animations import PlayerAnimations
from typing import Any
from values.sprite_groups import all_sprites, enemy_group
import pygame


# Базовый класс с коллизией
# коллизия просчитывается автоматически в дочерних классах нужно только переопределить метод move
# если нужно добавить логику в update() можно использовать super()
# или переопределить update но тогда добавить логику коллизий
class LiveObject(ActionAnimatedSprite):
    def __init__(self, pos: (int, int), actions, start_action_name, health, speed, tiles_group, opponent_group,
                 direction, *groups):
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
        self.opponent_group = opponent_group
        self.active_weapon = pygame.sprite.Group()
        self.is_invulnerable = False

    def creating_edges(self):
        creator_edges = CollisionsEdges((self.rect.x, self.rect.y), self.rect.height, self.rect.width)
        edges = creator_edges.creating_all_edges()
        self.top_edge = edges["top"]
        self.left_edge = edges["left"]
        self.right_edge = edges["right"]
        self.bottom_edge = edges["bottom"]

    def gravity(self, delta_t):
        if self.collision_directions["bottom"]:
            speed = 0
            if self.y_speed > 0:
                self.y_speed = 0
            else:
                if pygame.sprite.spritecollideany(self, self.tiles_group):
                    speed = -1
            self.rect.move_ip(0, speed)
            self.move_edges(0, speed)
        elif not self.collision_directions["bottom"]:
            if self.y_speed < MAX_GRAVITY_SPEED:
                self.y_speed += delta_t * GRAVITY

    def dead(self):
        if self.health <= 0:
            self.is_dead = True
            self.kill()

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
        if self.active_weapon:
            self.rect.move_ip(-self.x_speed, 0)
            self.move_edges(-self.x_speed, 0)
        self.collision_with_world()
        self.gravity(delta_t)
        self.dead()
        self.move()
        self.move_edges(self.x_speed, self.y_speed)


class Enemy(LiveObject):
    def __init__(self, pos, health, speed, weapon, cooldown_attack, tiles_group, opponent_group):
        self.setup()
        self.animations = {
            "idle_right": ActionAnimation(pygame.image.load("data/animations/characters/enemies/mushroom/idle.png"), 1,
                                          1, (60, 60), 60, RIGHT)
        }
        super().__init__(pos, self.animations, "idle_right", health, speed, tiles_group,
                         opponent_group, RIGHT, enemy_group, all_sprites)

        self.weapon = weapon
        self.right_attack_field = None
        self.left_attack_field = None
        self.ranged = None
        self.creating_field_view()
        self.creating_search_engine_void()
        self.creating_attack_field()
        self.x_speed = self.speed
        self.is_player_found = False
        self.timer_attack = 0
        self.cooldown_attack = cooldown_attack
        self.ready_attack = False

    def switch_direction_right(self):
        self.x_speed = self.speed
        self.direction = RIGHT

    def switch_direction_left(self):
        self.x_speed = -self.speed
        self.direction = LEFT

    def creating_field_view(self):
        creator_field_view = FieldViewEnemy(self.rect.center)
        field_view = creator_field_view.creating_all_field()
        self.right_field_view = field_view["right"]
        self.left_field_view = field_view["left"]
        self.vertical_field_view = field_view["vertical"]

    def creating_search_engine_void(self):
        creator = SearchVoid((self.rect.x, self.rect.y), self.rect.width, self.rect.height)
        all_search_engine = creator.creating_search_engine()
        self.right_search_engine_void = all_search_engine["right"]
        self.left_search_engine_void = all_search_engine["left"]

    def player_search(self):
        if not self.is_player_found:
            if collied_player := pygame.sprite.spritecollideany(self.left_field_view, self.opponent_group):
                if collied := pygame.sprite.spritecollideany(self.left_field_view, self.tiles_group):
                    if collied.rect.x < collied_player.rect.x:
                        self.x_speed = -self.speed
                        self.direction = LEFT
                        self.is_player_found = True
                else:
                    self.x_speed = -self.speed
                    self.direction = LEFT
                    self.is_player_found = True
            elif collied_player := pygame.sprite.spritecollideany(self.right_field_view, self.opponent_group):
                if collied := pygame.sprite.spritecollideany(self.right_field_view, self.tiles_group):
                    if collied.rect.x > collied_player.rect.x:
                        self.x_speed = self.speed
                        self.direction = RIGHT
                        self.is_player_found = True
                else:
                    self.x_speed = self.speed
                    self.direction = RIGHT
                    self.is_player_found = True

    def switch_direction_movement(self):
        if self.opponent_group:
            if self.direction == RIGHT:
                if pygame.sprite.collide_rect(self.vertical_field_view,
                                              self.opponent_group.sprites()[0].right_edge):
                    self.switch_direction_left()
            if self.direction == LEFT:
                if pygame.sprite.collide_rect(self.opponent_group.sprites()[0].left_edge,
                                              self.vertical_field_view):
                    self.switch_direction_right()

    def jump(self):
        if self.collision_directions["bottom"] and not self.active_weapon:
            if self.direction == RIGHT:
                if self.collision_directions["right"] or \
                        not pygame.sprite.spritecollideany(self.right_search_engine_void, self.tiles_group):
                    self.y_speed = JUMP_SPEED
            else:
                if self.collision_directions["left"] or \
                        not pygame.sprite.spritecollideany(self.left_search_engine_void, self.tiles_group):
                    self.y_speed = JUMP_SPEED

    def patrolling(self):
        if self.direction == RIGHT:
            if self.collision_directions["right"] or \
                    not pygame.sprite.spritecollideany(self.right_search_engine_void, self.tiles_group):
                self.switch_direction_left()
        if self.direction == LEFT:
            if self.collision_directions["left"] or \
                    not pygame.sprite.spritecollideany(self.left_search_engine_void, self.tiles_group):
                self.switch_direction_right()

    @alive_only
    def player_harassment(self):
        if not self.is_player_found:
            self.player_search()
            self.patrolling()
        else:
            self.switch_direction_movement()
            self.jump()
            self.attack()

    def move_field_view(self, x, y):
        self.vertical_field_view.rect.move_ip(x, y)
        self.right_field_view.rect.move_ip(x, y)
        self.left_field_view.rect.move_ip(x, y)

    def move_search_engine_void(self, x, y):
        self.right_search_engine_void.rect.move_ip(x, y)
        self.left_search_engine_void.rect.move_ip(x, y)

    def move_attack_field(self, x, y):
        self.right_attack_field.rect.move_ip(x, y)
        self.left_attack_field.rect.move_ip(x, y)

    def collision_with_world(self):
        self.get_collision_directions()
        if self.collision_directions["top"] and self.y_speed < 0:
            self.y_speed = 0
        if self.collision_directions["left"] and self.x_speed < 0:
            self.rect.move_ip(-self.x_speed, 0)
            self.move_edges(-self.x_speed, 0)
            self.move_field_view(-self.x_speed, 0)
            self.move_search_engine_void(-self.x_speed, 0)
            self.move_attack_field(-self.x_speed, 0)
        if self.collision_directions["right"] and self.x_speed > 0:
            self.rect.move_ip(-self.x_speed, 0)
            self.move_edges(-self.x_speed, 0)
            self.move_field_view(-self.x_speed, 0)
            self.move_search_engine_void(-self.x_speed, 0)
            self.move_attack_field(-self.x_speed, 0)

    def gravity(self, delta_t):
        if self.collision_directions["bottom"] \
                and self.y_speed > 0:
            speed = -self.y_speed * delta_t
            self.rect.move_ip(0, speed)
            self.move_edges(0, speed)
            self.move_field_view(0, speed)
            self.move_search_engine_void(0, speed)
            self.move_attack_field(0, speed)
            self.y_speed = 0
        else:
            if self.y_speed < MAX_GRAVITY_SPEED:
                self.y_speed += delta_t * GRAVITY

    def move(self):
        self.rect.move_ip(self.x_speed, self.y_speed)

    def update(self, delta_t, *args: Any, **kwargs: Any) -> None:
        super().update(delta_t)
        self.move_field_view(self.x_speed, self.y_speed)
        self.move_search_engine_void(self.x_speed, self.y_speed)
        self.move_attack_field(self.x_speed, self.y_speed)
        self.player_harassment()
        self.update_ready_attack(delta_t)
        if self.active_weapon:
            self.move_field_view(-self.x_speed, 0)
            self.move_search_engine_void(-self.x_speed, 0)
            self.move_attack_field(-self.x_speed, 0)

    def update_ready_attack(self, delta_t):
        if not self.ready_attack:
            self.timer_attack += delta_t
        if self.timer_attack >= self.cooldown_attack:
            self.timer_attack = 0
            self.ready_attack = True

    def attack(self):
        is_attack = False
        if self.collision_directions["bottom"]:
            if collied_player := pygame.sprite.spritecollideany(self.right_attack_field, self.opponent_group):
                if collied := pygame.sprite.spritecollideany(self.right_attack_field, self.tiles_group):
                    if collied.rect.x > collied_player.rect.x:
                        coefficient = self.rect.width
                        is_attack = True
                        direction = RIGHT
                else:
                    coefficient = self.rect.width
                    is_attack = True
                    direction = RIGHT
            elif collied_player := pygame.sprite.spritecollideany(self.left_attack_field, self.opponent_group):
                if collied := pygame.sprite.spritecollideany(self.left_attack_field, self.tiles_group):
                    if collied.rect.x < collied_player.rect.x:
                        coefficient = 0
                        direction = LEFT
                        is_attack = True
                else:
                    coefficient = 0
                    direction = LEFT
                    is_attack = True
            if is_attack:
                self.x_speed = 0
            else:
                self.x_speed = self.speed * self.direction
            if self.ready_attack and is_attack:
                pos = (self.rect.x + coefficient, self.rect.y + self.rect.height // 2)
                self.weapon.attack(pos, direction, self.active_weapon)
                self.ready_attack = False

    def creating_attack_field(self):
        pass

    def setup(self):
        pass


class EnemyWithCloseCombat(Enemy):

    def creating_attack_field(self):
        creator = AttackField(self.rect.center, self.weapon.rect.height, self.weapon.rect.height)
        all_field = creator.creating_field_attack()
        self.right_attack_field = all_field["right"]
        self.left_attack_field = all_field["left"]
        self.ranged = False


class EnemyWithRangedCombat(Enemy):

    def creating_attack_field(self):
        creator = AttackField(self.rect.center, self.weapon.flight_range, 1)
        all_field = creator.creating_field_attack()
        self.right_attack_field = all_field["right"]
        self.left_attack_field = all_field["left"]
        self.ranged = True
