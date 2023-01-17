import collections

import pygame

from basic_classes.initial_screen import InitialScreen
from camera import Camera
from values.constants import WIDTH, HEIGHT, FPS, TILE_SIZE
from level_work import generate_level, load_level
from values.sprite_groups import all_sprites, door_group, tiles_group, player_group, boxes_group, enemy_group, \
    active_weapons_group, enemy_shells
from utils import load_image


class Game:
    def __init__(self):
        self.running = False
        self.background = load_image("data/world/background.png")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.event_handlers = collections.defaultdict(list)
        self.player = None
        self.is_jump = False
        self.can_quit = False

    def setup(self):
        pass

    def register_event(self, event_type, action):
        self.event_handlers[event_type].append(action)

    def start(self):
        pygame.init()
        pygame.mixer.music.load('data/dooms_gate.wav')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.5)
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        start_screen = InitialScreen(screen)
        level_name = start_screen.start_screen()
        self.player = generate_level(load_level(level_name))
        self.running = True
        font = pygame.font.Font(None, 20)
        text1 = font.render('Чтобы перейти к выбору уровня нажмите "Q"', 1, (255, 0, 0))
        timer = pygame.time.Clock()
        self.register_event(pygame.KEYDOWN, self.player.start_move)
        self.register_event(pygame.KEYUP, self.player.stop_move)
        self.register_event(pygame.KEYDOWN, self.player.jump)
        self.register_event(pygame.MOUSEBUTTONDOWN, self.player.use_weapon)
        self.register_event(pygame.K_q, self.back_to_menu)
        camera = Camera()
        while self.running:
            delta_t = timer.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if callbacks := self.event_handlers[event.type]:
                    for callback in callbacks:
                        callback(event)
                if self.can_quit:
                    screen.blit(text1, (10, 50))
            # camera.update(self.player)
            screen.blit(self.background, (0, 0))
            all_sprites.draw(screen)
            self.update(screen, delta_t)
            # for sprite in all_sprites:
            #     camera.apply(sprite)
            pygame.display.flip()

    def update(self, surface, delta_t):
        if door_group.sprites()[0].rect.collidepoint(self.player.rect.x + TILE_SIZE * 2, self.player.rect.y)\
                or door_group.sprites()[0].rect.collidepoint(self.player.rect.x - TILE_SIZE * 2, self.player.rect.y):
            self.can_quit = True
        all_sprites.update(delta_t)

    def back_to_menu(self):
        if self.can_quit:
            self.restart()

    def restart(self):
        all_sprites.empty()
        tiles_group.empty()
        player_group.empty()
        boxes_group.empty()
        enemy_group.empty()
        active_weapons_group.empty()
        enemy_shells.empty()
        door_group.empty()
        self.start()


game = Game()
game.start()
