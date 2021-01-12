import pygame # 123
import os
import sys

FPS = 50
WIDTH = 500
HEIGHT = 500


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
    pass


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

    def update(self):
        pass

    def cut_sheet(self):
        pass


class Blocks(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_):
        super().__init__(blocks_group, all_sprites)


class Food(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_):
        super().__init__(blocks_group, all_sprites)

    def update(self):
        pass