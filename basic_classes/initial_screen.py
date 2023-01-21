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

    def terminate(self):
        pygame.quit()
        sys.exit()

    def start_screen(self):
        pygame.init()
        pygame.mixer.music.load('data/dooms_gate.wav')
        pygame.mixer.music.play(999)
        pygame.mixer.music.set_volume(0.5)
        self.intro_text = ['Выберите уровень:']
        for el in get_files_in_directory('maps'):
            self.intro_text.append(el)
        fon = pygame.transform.scale(load_image('data/initial_screen.jpg'), (WIDTH, HEIGHT))
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 70)
        text_coord = 50
        for line in self.intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            self.rects.append(intro_rect)
            self.buttons[line] = intro_rect
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 'txt' in str(self.get_chosen_level(pygame.mouse.get_pos())):
                        pygame.mixer.music.unload()
                        return self.get_chosen_level(pygame.mouse.get_pos())
            pygame.display.flip()
            clock.tick(FPS)

    def get_chosen_level(self, mouse_cords):
        for line in self.intro_text:
            if self.buttons[line].collidepoint(mouse_cords):
                return line
