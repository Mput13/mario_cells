import pygame
from pygame.sprite import AbstractGroup
from typing import Any


class Animated:
    TARGET_SIZE = 128, 128
    SPEED_PER_SEC = 12

    rect: pygame.Rect

    def __init__(self, sheet, columns, rows):
        self.frames: list[pygame.Surface] = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

        self.frame_counter = 0
        self.frame_delimiter = FPS // self.SPEED_PER_SEC

        self.single_play = False

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(
            0, 0, sheet.get_width() // columns,
                  sheet.get_height() // rows
        )
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)

                part = sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                part = pygame.transform.scale(part, self.TARGET_SIZE)
                self.frames.append(part)

        real_size = self.frames[0].get_size()
        self.rect = pygame.Rect(0, 0, *real_size)

    def reset(self):
        self.frame_counter = 0
        self.cur_frame = 0
        self.single_play = False

    def set_play_single(self):
        self.single_play = True

    def update(self):
        if self.frame_counter % self.frame_delimiter == 0:
            index = self.cur_frame + 1

            if self.single_play and index == len(self.frames):
                return

            self.cur_frame = index % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.frame_counter = 0

        self.frame_counter += 1


class ActionAnimation(Animated):
    def __init__(self, sheet, columns, rows, speed=None, *args):
        if speed:
            self.SPEED_PER_SEC = speed
        super().__init__(sheet, columns, rows)


class ActionAnimatedSprite(pygame.sprite.Sprite):
    RiGHT_ROTATED_ACTION_POSTFIX = '_right'
    LEFT_ROTATED_ACTION_POSTFIX = '_left'

    def __init__(
            self,
            pos: tuple[int, int],
            actions: dict[str, ActionAnimation],
            start_action_name: str,
            *groups: AbstractGroup,
            is_right_rotated: bool = True
    ):
        super().__init__(*groups)
        self.is_right_rotated = is_right_rotated
        if start_action_name not in actions:
            raise KeyError(f'Specified start animation not found. Available: {actions}')

        self.actions = actions
        self.current_animation = actions[start_action_name]
        self.current_animation_name = start_action_name

        self.image = self.current_animation.image
        self.rect = self.current_animation.rect
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def switch(self, name: str, single: bool = False):
        if name not in self.actions:
            raise KeyError(f'Specified animation not found. Available: {self.actions}')

        if name == self.current_animation_name:
            return
        self.current_animation.reset()
        self.current_animation = self.actions[name]
        self.current_animation_name = name

        if single:
            self.current_animation.set_play_single()

    def switch_undirected(self, name: str, single: bool = False):
        full_name = name + self.RiGHT_ROTATED_ACTION_POSTFIX if self.is_right_rotated else name + self.LEFT_ROTATED_ACTION_POSTFIX
        self.switch(full_name, single=single)

    def _horizontal_flip(self, is_right: bool):
        self.is_right_rotated = is_right
        if is_right:
            if not self.is_right_rotated:
                name = self.current_animation_name.replace(
                    self.LEFT_ROTATED_ACTION_POSTFIX,
                    self.RiGHT_ROTATED_ACTION_POSTFIX
                )
                self.switch(name)
        else:
            if self.is_right_rotated:
                name = self.current_animation_name.replace(
                    self.RiGHT_ROTATED_ACTION_POSTFIX,
                    self.LEFT_ROTATED_ACTION_POSTFIX
                )
                self.switch(name)

    def flip_right(self):
        self._horizontal_flip(is_right=True)

    def flip_left(self):
        self._horizontal_flip(is_right=False)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.current_animation.update()
        self.image = self.current_animation.image
