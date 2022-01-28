import json

import pygame
import random
import os

IMAGE_SIZE = 64
SIZE = (700, 650)
WIDTH, HEIGHT = SIZE[0] // IMAGE_SIZE, SIZE[1] // IMAGE_SIZE
counter = 0
FPS = 60
SPEED = 30

rotate = pygame.transform.rotate
skins = {"default": ["spine2.png", "head2.png"], "second": ["spine5.png", "head5.png"],
         "third": ["spine3.png", "head3.png"], "fourth": ["spine4.png", "head4.png"],
         "fifth": ["spine6.png", "head6.png"]}


def load_image(name, colorkey=None):
    fullname = os.path.join('pictures', name)
    image = pygame.image.load(fullname)
    return image


class Apple(pygame.sprite.Sprite):
    sprites = [load_image("apple.png"), load_image("apple2.png"), load_image("apple3.png"),
               load_image("apple4.png")]

    def __init__(self, x, y, *group):
        super().__init__(*group)

        self.image = Apple.sprites[random.randint(0, len(Apple.sprites) - 1)]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class SnakePiece(pygame.sprite.Sprite):
    with open("config.json", encoding="utf-8") as _f:
        _f = json.load(_f)
    _f = _f["skin"]
    SPRITE = load_image(skins[_f][0])
    HEAD = load_image(skins[_f][1])

    lst = []

    def __init__(self, *group, typo, coord, destination):
        super().__init__(*group)
        # self.image = typo
        self.rect = typo.get_rect()
        self.rect.x = coord[0] * IMAGE_SIZE
        self.rect.y = coord[1] * IMAGE_SIZE
        self.coord = coord
        SnakePiece.lst.append(self)
        self.destination = destination

        self.update_sprite(typo)

    def update_sprite(self, new_type):
        if self.destination == Snake.RIGHT:
            self.image = new_type
        elif self.destination == Snake.LEFT:
            self.image = rotate(new_type, 180)
        elif self.destination == Snake.UP:
            self.image = rotate(new_type, 90)
        elif self.destination == Snake.DOWN:
            self.image = rotate(new_type, -90)

    def rotate(self, angle):
        self.image = rotate(self.image, angle)


def change_image():
    with open("config.json", encoding="utf-8") as _f:
        _f = json.load(_f)
    _f = _f["skin"]
    SnakePiece.SPRITE = load_image(skins[_f][0])
    SnakePiece.HEAD = load_image(skins[_f][1])


class Snake:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __init__(self, game):
        self.sprite_group = pygame.sprite.Group()
        self.destination = Snake.RIGHT
        SnakePiece(self.sprite_group, typo=SnakePiece.SPRITE, coord=(WIDTH // 2 - 2, HEIGHT // 2),
                   destination=self.destination)
        SnakePiece(self.sprite_group, typo=SnakePiece.SPRITE, coord=(WIDTH // 2 - 1, HEIGHT // 2),
                   destination=self.destination)
        SnakePiece(self.sprite_group, typo=SnakePiece.HEAD, coord=(WIDTH // 2, HEIGHT // 2),
                   destination=self.destination)

        self.game = game

    def render(self, screen):
        self.sprite_group.draw(screen)

    def update(self):
        global counter
        # Изменение направления движения

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if self.destination != Snake.DOWN:
                self.destination = Snake.UP
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if self.destination != Snake.UP:
                self.destination = Snake.DOWN
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.destination != Snake.LEFT:
                self.destination = Snake.RIGHT
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.destination != Snake.RIGHT:
                self.destination = Snake.LEFT

        # Движение

        if counter % SPEED != 0:
            return

        counter = 0

        self.move_head()
        self.sprite_group.remove(self.sprite_group.sprites()[0])
        del SnakePiece.lst[0]
        SnakePiece.lst[0].update_sprite(SnakePiece.SPRITE)
        SnakePiece.lst[-2].update_sprite(SnakePiece.SPRITE)

        # Столкновение с едой
        if pygame.sprite.spritecollideany(self.sprite_group.sprites()[-1], self.game.eat):
            self.game.eat.empty()  # Змея хавает!
            SnakePiece.lst[-1].update_sprite(SnakePiece.SPRITE)
            self.game.add_score(1)
            self.move_head()

    def move_head(self):
        if self.destination == Snake.UP:
            SnakePiece(self.sprite_group, typo=SnakePiece.HEAD,
                       coord=(SnakePiece.lst[-1].coord[0], SnakePiece.lst[-1].coord[1] - 1),
                       destination=self.destination)
        elif self.destination == Snake.DOWN:
            SnakePiece(self.sprite_group, typo=SnakePiece.HEAD,
                       coord=(SnakePiece.lst[-1].coord[0], SnakePiece.lst[-1].coord[1] + 1),
                       destination=self.destination)
        elif self.destination == Snake.LEFT:
            SnakePiece(self.sprite_group, typo=SnakePiece.HEAD,
                       coord=(SnakePiece.lst[-1].coord[0] - 1, SnakePiece.lst[-1].coord[1]),
                       destination=self.destination)
        elif self.destination == Snake.RIGHT:
            SnakePiece(self.sprite_group, typo=SnakePiece.HEAD,
                       coord=(SnakePiece.lst[-1].coord[0] + 1, SnakePiece.lst[-1].coord[1]),
                       destination=self.destination)

    def check_ranges(self):
        flag = False
        for snake_piece in self.sprite_group:
            if snake_piece.rect.x + IMAGE_SIZE >= SIZE[0] + 50 or \
                    snake_piece.rect.x - IMAGE_SIZE < -IMAGE_SIZE or \
                    snake_piece.rect.y + IMAGE_SIZE >= SIZE[1] + 50 or \
                    snake_piece.rect.y - IMAGE_SIZE < -IMAGE_SIZE:
                flag = True
                break
        return flag

    def check_snake_self_intersections(self):
        if pygame.sprite.spritecollideany(self.sprite_group.sprites()[-1],
                                          pygame.sprite.Group(self.sprite_group.sprites()[:-2])):
            return True
        return False


class Game:
    def __init__(self):
        self.running = True

        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption('Snake')
        self.eat = pygame.sprite.Group()

        self.snake = Snake(self)

        self.clock = pygame.time.Clock()
        self.score = 0

    def run(self):
        global counter

        while self.running:
            counter += 1

            self.events()
            self.update()
            self.render()

            self.clock.tick(FPS)

    def update(self):
        if self.snake.check_ranges() or self.snake.check_snake_self_intersections():  # Отслеживание выхода за границы
            self.death_event()

        self.snake.update()

        if len(self.eat) == 0:
            x = random.randint(0, WIDTH - 1) * IMAGE_SIZE
            y = random.randint(0, HEIGHT - 1) * IMAGE_SIZE
            Apple(x, y, self.eat)

    def render(self):
        image = pygame.transform.scale(load_image('background.jpg'), (700, 650))
        self.screen.blit(image, (0, 0))

        self.snake.render(self.screen)
        self.eat.draw(self.screen)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def add_score(self, value):
        self.score += value
        pygame.display.set_caption(f'Snake: {self.score}')

    def death_event(self):
        print("Едрить-колотить, кажется, это смерть!")
        self.running = False


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()