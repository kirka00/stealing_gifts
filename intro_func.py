from intro import Menu


def intro_func():  # в punkts 1 корды потом что будет написано и 2 кортежа в 1 цвет когда не выбраны а во 2 когда выбраны ласт номер
    punkts = [(120, 70, u'Game', (41, 49, 51), (76, 81, 74), 0),  # запуск
              (120, 140, u'Settings', (41, 49, 51), (76, 81, 74), 1),  # настройки
              (120, 210, u'Quit', (41, 49, 51), (76, 81, 74), 2),  # выход
              (120, 280, u'Support', (41, 49, 51), (76, 81, 74), 3)]  # поддержка
    game = Menu(punkts)
    game.menu()