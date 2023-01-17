import collections

from basic_classes.initial_screen import InitialScreen
import sys
import pygame
from camera import Camera
from values.constants import WIDTH, HEIGHT, FPS, GRAVITY, TILE_SIZE
from level_work import generate_level, load_level
from values.sprite_groups import all_sprites, tiles_group, door_group
from utils import load_image, get_path, get_files_in_directory


class Game:
    def __init__(self):
        self.running = False
        self.background = load_image("data/background.png")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.event_handlers = collections.defaultdict(list)
        self.can_quit = False
        self.player = None
        self.is_jump = False

    def setup(self):
        pass

    def register_event(self, event_type, action):
        self.event_handlers[event_type].append(action)

    def start(self):
        pygame.init()
        pygame.mixer.music.load('data/dooms_gate.wav')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.5)
        jump_sound = pygame.mixer.Sound('data/jump_sound.wav')
        jump_sound.set_volume(0.1)
        self.death_sound = pygame.mixer.Sound('data/death_sound.wav')
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        start_screen = InitialScreen(screen)
        level_name = start_screen.start_screen()
        camera = Camera()
        x = generate_level(load_level(f'maps/{level_name}'))
        self.player = x[0]
        self.max_y = x[1]
        self.running = True
        timer = pygame.time.Clock()
        self.running = True
        pygame.init()
        font = pygame.font.Font(None, 20)
        text1 = font.render('Чтобы перейти к выбору уровня нажмите "Q"', 1, (255, 0, 0))
        while self.running:
            key = pygame.key.get_pressed()
            delta_t = timer.tick(FPS) / 1000
            if key[pygame.K_a]:
                self.player.move(delta_t, left=True)
            if key[pygame.K_d]:
                self.player.move(delta_t, right=True)
            if key[pygame.K_SPACE] and pygame.sprite.spritecollideany(self.player, tiles_group):
                jump_sound.play()
                self.is_jump = True
                self.player.rect.y -= 10
                self.player.y_speed = -750
            if key[pygame.K_q] and self.can_quit:
                self.restart()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if callbacks := self.event_handlers[event.type]:
                    for callback in callbacks:
                        callback(event)
            camera.update(self.player)
            # обновляем положение всех спрайтов
            for sprite in all_sprites:
                camera.apply(sprite)
            screen.blit(self.background, (0, 0))
            if self.can_quit:
                screen.blit(text1, (10, 50))
            all_sprites.draw(screen)
            self.update(screen, delta_t)
            pygame.display.flip()

    def update(self, surface, delta_t):
        if self.player.rect.y > self.max_y + 200:
            self.death_sound.play()
            self.restart()
        if door_group.sprites()[0].rect.collidepoint(self.player.rect.x + TILE_SIZE * 2, self.player.rect.y):
            self.can_quit = True
        else:
            self.can_quit = False
        if self.is_jump:
            if pygame.sprite.spritecollideany(self.player, tiles_group):
                self.is_jump = False
            else:
                self.player.move(delta_t)
                self.player.y_speed += delta_t * 2000
        else:
            if pygame.sprite.spritecollideany(self.player, tiles_group):
                self.is_jump = False
                self.player.y_speed = GRAVITY
            else:
                self.player.move(delta_t, down=True)
                self.player.y_speed -= delta_t * 1000

    def restart(self):
        all_sprites.empty()
        door_group.empty()
        tiles_group.empty()
        self.start()

    def terminate(self):
        pygame.quit()
        sys.exit()
