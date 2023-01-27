import pygame.image
from values.constants import RIGHT, LEFT
from basic_classes.for_live_object_and_enemy import EnemyWithCloseCombat, EnemyWithRangedCombat
from basic_classes.for_animation import ActionAnimation


class MushroomCloseCombat(EnemyWithCloseCombat):
    def setup(self):
        self.animations = {
            "walk_right": ActionAnimation(pygame.image.load("data/animations/characters/enemies/mushroom/walk.png"), 2,
                                          1, (60, 60), 30, RIGHT),
            "walk_left": ActionAnimation(
                pygame.transform.flip(pygame.image.load("data/animations/characters/enemies/mushroom/walk.png"),
                                      flip_x=True, flip_y=False), 2, 1, (60, 60), 30, LEFT),
            "idle_right": ActionAnimation(pygame.image.load("data/animations/characters/enemies/mushroom/idle.png"), 1,
                                          1, (60, 60), 60, RIGHT),
            "idle_left": ActionAnimation(
                pygame.transform.flip(pygame.image.load("data/animations/characters/enemies/mushroom/idle.png"),
                                      flip_x=True, flip_y=False), 1, 1, (60, 60), 60, LEFT)
        }
