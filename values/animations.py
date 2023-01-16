import enum
from basic_classes.for_animation import ActionAnimation
import pygame
from values.constants import RIGHT, LEFT


class BowAnimations(enum.Enum):
    shot_right = ActionAnimation(pygame.image.load("data/animations/weapons/bow_shot.png"), 6, 4, (35, 45), 60, RIGHT)
    shot_left = ActionAnimation(
        pygame.transform.flip(pygame.image.load("data/animations/weapons/bow_shot.png"), flip_x=True, flip_y=False),
        6, 4, (35, 45), 60, LEFT)


class PlayerAnimations(enum.Enum):
    walk_right = ActionAnimation(pygame.image.load("data/animations/characters/player/walk.png"),
                                 3, 1, (58, 58), 20, RIGHT)
    walk_left = ActionAnimation(
        pygame.transform.flip(pygame.image.load("data/animations/characters/player/walk.png"), flip_x=True,
                              flip_y=False), 3, 1, (58, 58), 20, LEFT)
    dead_right = ActionAnimation(pygame.image.load("data/animations/characters/player/dead.png"),
                                 1, 1, (58, 58), 60, RIGHT)
    dead_left = ActionAnimation(
        pygame.transform.flip(pygame.image.load("data/animations/characters/player/dead.png"), flip_x=True,
                              flip_y=False), 1, 1, (58, 58), 60, LEFT)
    idle_right = ActionAnimation(pygame.image.load("data/animations/characters/player/idle.png"),
                                 1, 1, (58, 58), 60, RIGHT)
    idle_left = ActionAnimation(
        pygame.transform.flip(pygame.image.load("data/animations/characters/player/idle.png"), flip_x=True,
                              flip_y=False), 1, 1, (58, 58), 60, LEFT)
    jump_right = ActionAnimation(pygame.image.load("data/animations/characters/player/jump.png"),
                                 1, 1, (60, 60), 60, RIGHT)
    jump_left = ActionAnimation(
        pygame.transform.flip(pygame.image.load("data/animations/characters/player/jump.png"), flip_x=True,
                              flip_y=False), 1, 1, (58, 58), 60, LEFT)
