import pygame

pygame.init()
jump_sound = pygame.mixer.Sound('data/jump_sound.ogg')
jump_sound.set_volume(0.1)
death_sound = pygame.mixer.Sound('data/death_sound.ogg')
sword_sound = pygame.mixer.Sound('data/sword.wav')
bow_sound = pygame.mixer.Sound('data/bow.ogg')