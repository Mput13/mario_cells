import os
import sys

import pygame

from utils import load_image, get_files_in_directory
from values.constants import WIDTH, HEIGHT, FPS


class InitialScreen:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = {}
        self.rects = []
        self.intro_text = ''
        self.chosen_weapon = []

    def terminate(self):
        pygame.quit()
        sys.exit()

    def start_screen(self):
        pygame.init()
        pygame.mixer.music.load('data/dooms_gate.ogg')
        pygame.mixer.music.play(999)
        pygame.mixer.music.set_volume(0.5)
        clock = pygame.time.Clock()
        self.add_text()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    chosen = str(self.get_chosen_level(pygame.mouse.get_pos()))
                    if 'txt' in chosen:
                        if len(self.chosen_weapon) == 2:
                            pygame.mixer.music.unload()
                            return self.get_chosen_level(pygame.mouse.get_pos()), self.chosen_weapon
                    elif chosen in ('bow', 'shield_right_click', 'sword', 'shield_left_click'):
                        if chosen in self.chosen_weapon:
                            self.chosen_weapon.remove(chosen)
                            self.add_text()
                        elif len(self.chosen_weapon) <= 1 and chosen not in self.chosen_weapon:
                            self.chosen_weapon.append(chosen)
                            self.add_text()
            pygame.display.flip()
            clock.tick(FPS)

    def add_text(self):
        self.intro_text = ['Выберите уровень:']
        for el in get_files_in_directory('maps'):
            self.intro_text.append(el)
        self.intro_text.append('Выберите 2 орудия:')
        self.intro_text.append('bow')
        self.intro_text.append('sword')
        self.intro_text.append('shield_right_click')
        self.intro_text.append('shield_left_click')
        fon = pygame.transform.scale(load_image('data/initial_screen.jpg'), (WIDTH, HEIGHT))
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 70)
        text_coord = 50
        for line in self.intro_text:
            if line in self.chosen_weapon:
                string_rendered = font.render(line, 1, pygame.Color('green'))
            else:
                string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            self.rects.append(intro_rect)
            self.buttons[line] = intro_rect
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

    def get_chosen_level(self, mouse_cords):
        for line in self.intro_text:
            if self.buttons[line].collidepoint(mouse_cords):
                return line
