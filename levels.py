from race import racing
import pygame
from settings import small_font, load_image, load_level
from json import dump
flag_on_lvl2 = True


class BlockBricks(pygame.sprite.Sprite):  # класс для платформ
    def __init__(self, width, height):
        super().__init__()
        self.image = load_image('brick.png')  # изображение платформы
        self.rect = self.image.get_rect()  # установка размеров
        self.rect.width, self.rect.height = width, height


class Bottle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('bottle.png')  # изображение платформы
        self.rect = self.image.get_rect()  # установка размеров


class Presents(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('present.png')  # изображение платформы
        self.rect = self.image.get_rect()  # установка размеров


class Station(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = load_image('station.png')  # изображение платформы
        self.rect = self.image.get_rect()  # установка размеров
        self.rect.width, self.rect.height = width, height


class Level(object):  # класс для уровня
    def __init__(self, player, name):
        self.coins = 0  # монеты или же очки
        self.player = player  # сам игрок
        self.platforms = pygame.sprite.Group()  # группа спрайтов
        self.cookies = pygame.sprite.Group()
        self.presents = pygame.sprite.Group()
        # 0 - труба 1 - печенька 2 - подарок 3, 4 - очки за подарок, печенье
        self.coords_objects = [(), (), (), 10, 20]
        lvl_1 = load_level(name)  # преобразование уровня в текст
        for i in range(len(lvl_1)):
            for j in range(len(lvl_1[i])):
                if lvl_1[i][j] != '2' and lvl_1[i][j] != '3' and lvl_1[i][j] != '0':
                    if lvl_1[i][j] == '1':
                        block = BlockBricks(32, 32)
                    elif lvl_1[i][j] == '6':
                        block = Station(0, 0)
                        # добавление координат трубы
                        self.coords_objects[0] = (j, i)
                    elif lvl_1[i][j] == '9':
                        block = BlockBricks(0, 0)
                    block.rect.x, block.rect.y = j * 32, i * 32 + 24  # координата x и y
                    self.platforms.add(block)  # добавление в группу
                elif lvl_1[i][j] == '2':
                    cok = Bottle()
                    cok.rect.x, cok.rect.y = j * 32, i * 32 + 24  # координата x и y
                    self.cookies.add(cok)  # добавление в группу
                    # добавление координат печеньки
                    self.coords_objects[1] = (j, i - 1)
                elif lvl_1[i][j] == '3':
                    pres = Bottle()
                    pres.rect.x, pres.rect.y = j * 32, i * 32 + 24   # координата x и y
                    self.presents.add(pres)  # добавление в группу
                    # добавление координат подарка
                    self.coords_objects[2] = (j, i - 1)

    def draw(self, screen):  # рисовка объектов
        screen.blit(load_image('backgame.png'), (0, 0))  # задний фон
        self.platforms.draw(screen)  # отрисовка блоков
        self.cookies.draw(screen)  # отрисовка печенек
        self.presents.draw(screen)  # отрисовка подарков

    def update(self):  # обновление экрана
        self.platforms.update()

    def clear(self):  # очистка уровня для инициализации нового
        self.platforms.remove()
        self.cookies.remove()
        self.presents.remove()

    def cookies_delete(self):  # remove не работает выходит только через kill
        for i in self.cookies:
            i.kill()

    def presents_delete(self):  # remove не работает выходит только через kill
        for i in self.presents:
            i.kill()

    def coords(self):
        return self.coords_objects

    def render_coins(self, screen):  # отображение монет
        conclusion = small_font.render(
            f'Количество очков: {self.coins}', True, 'black')
        screen.blit(conclusion, (100, 120))

    def change_coins(self, coin):
        self.coins += coin
        save_in_coins_txt(self.coins)  # сохранение монет в текстовый файл


def check(coords, lvl):  # проверка для перехода на след лвл
    global flag_on_lvl2
    cor, cor1 = (coords[0] // 32, (coords[1] - 24) //
                 32), lvl.coords()  # преобразовка для удобства
    if cor == cor1[1]:  # проверка находится ли игрок на печеньке
        lvl.change_coins(cor1[4])  # добавление очков
        lvl.coords_objects[4] = 0
        lvl.cookies_delete()
    elif cor == cor1[2]:  # проверка находится ли игрок на подарке
        lvl.change_coins(cor1[3])   # добавление очков
        lvl.coords_objects[3] = 0
        lvl.presents_delete()
    elif cor == cor1[0]:  # проверка находится ли игрок на трубе
        lvl.change_coins(30)
        if not flag_on_lvl2:  # костыль убрать надо
            racing()
        else:
            flag_on_lvl2 = False
            return True


def save_in_coins_txt(coins):  # сохранение очков в coins.txt
    with open('coins.txt', encoding='utf8', mode='w') as file:
        dump(coins, file)