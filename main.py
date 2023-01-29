import collections

import pygame
from time import time
from basic_classes.initial_screen import InitialScreen
from camera import Camera
from sounds import death_sound
from values.constants import WIDTH, HEIGHT, FPS, TILE_SIZE
from level_work import generate_level, load_level
from values.sprite_groups import all_sprites, door_group, tiles_group, player_group, boxes_group, enemy_group, \
    active_weapons_group, enemy_shells, invisible_objects_group, hollow_group
from utils import load_image


# rssrt
class Game:
    def __init__(self):
        self.running = False
        self.background = load_image("data/world/background.png")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.event_handlers = collections.defaultdict(list)
        self.player = None
        self.is_jump = False
        self.can_quit = False
        self.max_y = 999999
        self.last_use = time()
        self.is_dash = False
        self.main_font = pygame.font.Font(None, 50)
        self.alert_font = pygame.font.Font(None, 20)
        self.last_health = None

    def setup(self):
        pass

    def register_event(self, event_type, action):
        self.event_handlers[event_type].append(action)

    def start(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        start_screen = InitialScreen(screen)
        sc = start_screen.start_screen()
        level_name = sc[0]
        pygame.init()
        pygame.mixer.music.load('data/fear.ogg')
        pygame.mixer.music.play(999)
        pygame.mixer.music.set_volume(0.1)
        self.player = generate_level(load_level(level_name), sc[1])
        self.running = True
        text1 = self.alert_font.render('Чтобы перейти к выбору уровня нажмите "Q"', 1, (0, 255, 100))
        timer = pygame.time.Clock()
        self.register_event(pygame.KEYDOWN, self.player.start_move)
        self.register_event(pygame.KEYUP, self.player.stop_move)
        self.register_event(pygame.KEYDOWN, self.player.jump)
        self.register_event(pygame.MOUSEBUTTONDOWN, self.player.use_weapon)
        camera = Camera()
        while self.running:
            self.last_health = self.player.health
            delta_t = timer.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if callbacks := self.event_handlers[event.type]:
                    for callback in callbacks:
                        callback(event)
            key = pygame.key.get_pressed()
            if key[pygame.K_q] and self.can_quit:
                self.restart()
            if key[pygame.K_e] and not self.is_dash and time() - self.last_use >= 0.9:
                self.is_dash = True
                self.player.x_speed *= 5
                self.last_use = time()
            if time() - self.last_use >= 0.1 and self.is_dash:
                self.player.x_speed //= 5
                self.is_dash = False
            if self.is_dash and self.player.health < self.last_health:
                self.player.health = self.last_health
            camera.update(self.player)
            screen.blit(self.background, (0, 0))
            if self.can_quit:
                screen.blit(text1, (10, 50))
            self.update_text(screen)
            all_sprites.draw(screen)
            self.update(screen, delta_t)
            for sprite in all_sprites:
                camera.apply(sprite)
            for sprite in invisible_objects_group:
                camera.apply(sprite)
            pygame.display.flip()

    def update(self, surface, delta_t):
        if self.player.health <= 0:
            death_sound.play()
            self.restart()
        if door_group.sprites()[0].rect.collidepoint(self.player.rect.x + TILE_SIZE * 2, self.player.rect.y) \
                or door_group.sprites()[0].rect.collidepoint(self.player.rect.x - TILE_SIZE * 2, self.player.rect.y):
            self.can_quit = True
        else:
            self.can_quit = False
        if pygame.sprite.spritecollideany(self.player, hollow_group):
            death_sound.play()
            self.restart()
        all_sprites.update(delta_t)

    def restart(self):
        hollow_group.empty()
        all_sprites.empty()
        tiles_group.empty()
        player_group.empty()
        boxes_group.empty()
        enemy_group.empty()
        active_weapons_group.empty()
        enemy_shells.empty()
        door_group.empty()
        pygame.mixer.music.unload()
        self.start()

    def update_text(self, screen):
        health = self.main_font.render(str(self.player.health), 1, (255, 0, 0))
        screen.blit(health, (0, 0))

game = Game()
game.start()
