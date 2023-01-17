import pygame

pygame.init()
jump_sound = pygame.mixer.Sound('data/jump_sound.wav')
jump_sound.set_volume(0.1)
death_sound = pygame.mixer.Sound('data/death_sound.wav')