import enum
from basic_classes.basic_classes_for_animation import ActionAnimation
import pygame
from values.constants import RIGHT, LEFT


class BowAnimations(enum.Enum):
    shot_right = ActionAnimation(pygame.image.load("./data/bow_shot.png"), 6, 4, (35, 45), 30, RIGHT)
    shot_left = ActionAnimation(
        pygame.transform.flip(pygame.image.load("./data/bow_shot.png"), flip_x=True, flip_y=False),
        6, 4, (35, 45), 30, LEFT)
