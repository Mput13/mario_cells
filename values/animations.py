import enum
from basic_classes.basic_classes_for_animation import ActionAnimation
import pygame
from values.constants import RIGHT, LEFT


class BowAnimations(enum.Enum):
    shot_right = ActionAnimation(pygame.image.load("data/animations/weapons/bow_shot.png"), 6, 4, (35, 45), 30, RIGHT)
    shot_left = ActionAnimation(
        pygame.transform.flip(pygame.image.load("data/animations/weapons/bow_shot.png"), flip_x=True, flip_y=False),
        6, 4, (35, 45), 30, LEFT)


class PlayerAnimations(enum.Enum):
    walk_right = ActionAnimation(pygame.image.load("data/animations/characters/player/mario_walk.png"),
                                 3, 1, (60, 60), 60, RIGHT)
    walk_left = ActionAnimation(
        pygame.transform.flip(pygame.image.load("data/animations/characters/player/mario_walk.png"), flip_x=True,
                              flip_y=False), 3, 1, (60, 60), 60, LEFT)
    dead_right = ActionAnimation(pygame.image.load("data/animations/characters/player/mario_dead.png"),
                                 1, 1, (60, 60), 60, RIGHT)
    dead_left = ActionAnimation(
        pygame.transform.flip(pygame.image.load("data/animations/characters/player/mario_dead.png"), flip_x=True,
                              flip_y=False), 1, 1, (60, 60), 60, LEFT)
    idle_right = ActionAnimation(pygame.image.load("data/animations/characters/player/mario.png"),
                                 1, 1, (60, 60), 60, RIGHT)
    idle_left = ActionAnimation(
        pygame.transform.flip(pygame.image.load("data/animations/characters/player/mario.png"), flip_x=True,
                              flip_y=False), 1, 1, (60, 60), 60, LEFT)
    jump_right = ActionAnimation(pygame.image.load("data/animations/characters/player/mario_jump.png"),
                                 1, 1, (60, 60), 60, RIGHT)
    jump_left = ActionAnimation(
        pygame.transform.flip(pygame.image.load("data/animations/characters/player/mario_jump.png"), flip_x=True,
                              flip_y=False), 1, 1, (60, 60), 60, LEFT)
