import pygame
import os
import sys
import random

FPS = 180
WIDTH = 700
HEIGHT = 700

score = 0


def game_over():
    global score
    intro_text = [f"Твой счёт: {score}", "Нажми, чтобы начать заново"]

    fon = pygame.transform.scale(load_image('game_over.jpg'), (WIDTH, HEIGHT))
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

    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return NyanCat(pic, 3, 3, 30, 100)

        pygame.display.flip()
        clock.tick(FPS)


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


class Blocks(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(blocks_group, all_sprites)
        width = random.randint(50, 150)
        self.image = pygame.Surface((width, 20))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        pygame.draw.rect(screen, pygame.Color("red"), (pos_x, pos_y, width, 20))

    def update(self):
        self.rect = self.rect.move(-2, 0)
        if self.rect.x + self.rect.width < 0:
            self.kill()


class Food(pygame.sprite.Sprite):
    images = ['eggs.png', 'fastfood.png', 'taco.png', 'burger.png', 'chocolate.png', 'cinnamon.png', 'cookie.png',
              'pancakes.png', 'pizza.png', 'sushi.png', 'taco2.png']
    def __init__(self, pos_x, pos_y):
        super().__init__(food_group, all_sprites)
        self.image = load_image(random.choice(Food.images))
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        global score
        self.rect = self.rect.move(-2, 0)
        if pygame.sprite.spritecollideany(self, player_group):
            score += 1
            self.kill()
        if self.rect.x + self.rect.width < 0:
            self.kill()


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
        self.jumping = False
        self.standing = False

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
                    if (block.rect.x <= self.rect.x + self.rect.width <= block.rect.x + block.rect.width or\
                           block.rect.x <= self.rect.x + 93 <= block.rect.x + block.rect.width)\
                            and block.rect.y <= self.rect.y + self.rect.height:
                        self.jump_counter = 0
                        self.standing = True
                    else:
                        self.standing = False
                    # это делаем булевой переменной, а потом при движении проверяем ее

        if self.jumping and pygame.sprite.spritecollideany(self, blocks_group) and self.rect.x > 0:
            self.rect = self.rect.move(0, -5)
        elif self.jumping and self.rect.x > 0:
            self.rect = self.rect.move(0, -10)

    def move(self):
        if not self.standing:
            self.rect = self.rect.move(0, 5)


class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bomb_group, all_sprites)
        self.image = load_image('bomb.png')
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        self.rect = self.rect.move(-2, 0)
        if self.rect.x + self.rect.width < 0:
            self.kill()
        if pygame.sprite.spritecollideany(self, player_group):
            cat.kill()
            game_over()

    def delete(self, event):
        global score
        if event and event.type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(event.pos):
            score += 2
            self.kill()


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
    bomb_group = pygame.sprite.Group()

    pic = pygame.transform.scale(load_image("nyan cat.png"), (567, 279))
    cat = NyanCat(pic, 3, 3, 30, 100)
    # kostyl = Invisible(30, 10)

    counter = 0
    jump_counter = 0
    running = True
    last = 0
    while running:
        counter += 1
        fon = pygame.transform.scale(load_image('fon_game.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

        if cat.jumping:
            jump_counter += 1
        if jump_counter > 70:
            cat.jumping = False
            jump_counter = 0

        if counter > 30:
            counter = 0
            y = random.randint(0, HEIGHT)
            while last - 100 < y < last + 100:
                y = random.randint(0, HEIGHT)
            last = y
            block = Blocks(WIDTH, y)
            food = Food(WIDTH, random.randint(0, HEIGHT))
            bomb = Bomb(WIDTH, random.randint(0, HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if cat.jump_counter < 2:
                    cat.jumping = True
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                cat.jump_counter += 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in bomb_group:
                    sprite.delete(event)

        all_sprites.draw(screen)
        all_sprites.update()
        cat.move()
        if not cat.alive():
            cat = game_over()

        pygame.display.flip()
        clock.tick(FPS)
