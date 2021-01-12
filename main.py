import pygame
import os
import sys
import random

FPS = 50
WIDTH = 600
HEIGHT = 600


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["NYAN CAT", "",
                  "Правила игры",
                  "Нажми пробел для прыжка",
                  "Собирай еду"]

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(247, 211, 162))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)


class NyanCat(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(pos_x, pos_y)

    def update(self):
        pass

    def cut_sheet(self):
        pass


class Blocks(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(blocks_group, all_sprites)
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class Food(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(blocks_group, all_sprites)

    def update(self):
        pass



if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Nyan Cat')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    start_screen()

    all_sprites = pygame.sprite.Group()
    blocks_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    running = True
    while running:
        block = Blocks(WIDTH, random.randint(0, HEIGHT))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(FPS)
