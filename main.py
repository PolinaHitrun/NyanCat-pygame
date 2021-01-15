import pygame
import os
import sys
import random

FPS = 180
WIDTH = 700
HEIGHT = 700


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
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


# class Camera:
#     # зададим начальный сдвиг камеры
#     def __init__(self):
#         self.dx = 0
#
#     # сдвинуть объект obj на смещение камеры
#     def apply(self, obj):
#         obj.rect.x += self.dx
#
#     # позиционировать камеру на объекте target
#     def update(self, target):
#         self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)

class Blocks(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(blocks_group, all_sprites)
        width = random.randint(50, 150)
        self.image = pygame.Surface((width, 20))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        pygame.draw.rect(screen, pygame.Color("red"), (pos_x, pos_y, width, 20))


    def update(self):
        self.rect = self.rect.move(-2, 0)


class Food(pygame.sprite.Sprite):
    images = ['eggs.png', 'fastfood.png', 'taco.png']

    def __init__(self, pos_x, pos_y):
        super().__init__(food_group, all_sprites)
        self.image = load_image(random.choice(Food.images))
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y

    def move(self):
        pass

    def update(self):
        self.rect = self.rect.move(-2, 0)


class NyanCat(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(player_group, all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.num = 0
        self.jump_counter = 0
        self.score = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.num += 1
        if self.num == FPS // 20:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.num = 0
            self.image = self.frames[self.cur_frame]
        # self.rect = self.rect.move(0, 3)
        if pygame.sprite.spritecollideany(self, blocks_group):
            for block in blocks_group:
                group = pygame.sprite.Group()
                group.add(block)
                if pygame.sprite.spritecollideany(self, group):
                    # если прыгает на платформу
                    if block.rect.x <= self.rect.x + self.rect.width <= block.rect.x + block.rect.width\
                            and block.rect.y >= self.rect.y + self.rect.height:
                        pass
                    else:
                        pass
                    # это делаем булевой переменной, а потом при движении проверяем ее



class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(food_group, all_sprites)
        self.image = load_image('bomb.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        self.rect = self.rect.move(-2, 0)



if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Nyan Cat')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    start_screen()
    fon = pygame.transform.scale(load_image('fon_game.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    all_sprites = pygame.sprite.Group()
    food_group = pygame.sprite.Group()
    blocks_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    cat = NyanCat(load_image("nyan cat.png") , 3 , 3 , 100 , 100)

    counter = 0
    running = True
    while running:
        counter += 1
        fon = pygame.transform.scale(load_image('fon_game.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        if counter > 20:
            counter = 0
            block = Blocks(WIDTH, random.randint(0, HEIGHT))
            food = Food(WIDTH, random.randint(0, HEIGHT))
            bomb = Bomb(WIDTH, random.randint(0, HEIGHT))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        blocks_group.update()
        food_group.update()
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
