import pygame
from settings import scr_height, load_image


class Player(pygame.sprite.Sprite):  # класс главного героя
    image = load_image('santa.png')  # изображение главного героя

    def __init__(self):
        super().__init__()
        self.right = True  # изначально герой повернут вправо
        self.hero_image = Player.image
        print(self.hero_image.get_rect())
        self.rect = self.hero_image.get_rect()  # размеры игрока
        self.score_x = 0  # векторы скорости игрока
        self.score_y = 0

    def gravity(self):  # гравитация
        self.score_y += 1
        if self.score_y >= 0 and self.rect.y >= scr_height - self.rect.height:
            self.score_y = 0    # смена значения у на 0, при нахождении на "земле"
            self.rect.y = scr_height - self.rect.height

    def jump(self):  # прыжок
        self.rect.y += 10  # проверяем, есть ли что-то под героем
        collide = pygame.sprite.spritecollide(
            self, self.level.platforms, False)  # проверка на коллизию
        self.rect.y -= 10  # возращение на исходную позицию
        if len(collide) > 0:
            self.score_y = -16   # прыгаем, если ничего не мешает

    def go_to_left(self):  # движение игрока влево
        self.score_x = -10  # Двигаем игрока влево по Х
        if self.right:  # проверка на то, куда он смотрит
            self.flip()  # если нужно, то переворачиваем
            self.right = False

    def go_to_right(self):  # движение игрока вправо
        self.score_x = 10  # Двигаем игрока вправо по Х
        if not self.right:  # проверка на то, куда он смотрит
            self.flip()  # если нужно, то переворачиваем
            self.right = True

    def stop(self):  # остновка движения
        self.score_x = 0

    def update(self):  # передвижение игрока
        self.gravity()  # гравитация
        self.rect.y += self.score_y  # передвижение вверх или вниз
        blocks_collide = pygame.sprite.spritecollide(
            self, self.level.platforms, False)  # слежка за препятствиями по вертикали
        for block in blocks_collide:  # установка нужных сторон по вертикали
            if self.score_y > 0:  # если вверх
                self.rect.bottom = block.rect.top
            elif self.score_y < 0:  # если вниз
                self.rect.top = block.rect.bottom
            self.score_y = 0  # остановка движения
        self.rect.x += self.score_x  # передвижение вправо
        blocks_collide = pygame.sprite.spritecollide(
            self, self.level.platforms, False)  # слежка за препятствиями по горизонтали
        for block in blocks_collide:  # установка нужных сторон по горизонтали
            if self.score_x > 0:  # если вправо
                self.rect.right = block.rect.left
            elif self.score_x < 0:  # если влево
                self.rect.left = block.rect.right

    def flip(self):  # отражение изображения при повороте
        self.image = pygame.transform.flip(self.image, True, False)