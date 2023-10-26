import random
from board import Board
from ship import Dot, Ship
from random import randint


class Player:
    def __init__(self, max_x, max_y):
        self.my_board = Board(max_x, max_y)  # Собственная доска
        self.enemy_board = Board(max_x, max_y)  # Доска врага
        self.shots = self.generate_shots()  # список выстрелов

    def generate_shots(self):
        res = []

        for y in range(self.enemy_board.max_y):
            for x in range(self.enemy_board.max_x):
                res.append(Dot(x, y))

        return res

    # спрашивает» игрока, в какую клетку он делает выстрел
    # возвращает Dot
    def ask(self):
        resultat = {"dot": None, "error": ""}
        error_ = ""

        while True:
            print(error_)
            # xy = input("Введите координаты выстрела XY (0 - остановить игру): ")
            xy = input("Введите координаты выстрела XY: ")
            # Проверим введено ли нужные координаты
            error_ = ""
            # if xy == "0":
            #     error_ = "Завершено"
            #     break
            if not xy.isnumeric():
                error_ = "Вводите только числа"
                continue
            elif xy == "":
                continue
            elif len(xy) != 2:
                error_ = "Введите координаты в формате XY"
                continue
            else:
                resultat["dot"] = Dot(int(xy[0]) - 1, int(xy[1]) - 1)
                break

        resultat["error"] = error_

        return resultat

    # делает ход в игре
    def move(self):

        # double_shot = False  # требуется повторный выстрел
        res = {"double_shot": False, "comment": "", 'alive': 0}

        shot_dot = self.ask()
        shot_ = self.enemy_board.shot(shot_dot['dot'])
        res["comment"] = f"выстрел {shot_dot['dot'].x + 1}:{shot_dot['dot'].y + 1}, " + shot_["comment"]
        res["double_shot"] = shot_["repeat"]
        res["alive"] = shot_["alive"]

        # убитый корабль, надо убрать выстрелы вокруг, чтобы не использовать больше их
        # if shot_["ship_dot"] != None:
        #     for dot_ in shot_["ship_dot"]:
        #         y_ = 0
        #         for yy_ in range(3):
        #             x_ = 0
        #             for xx_ in range(3):
        #                 x_ = dot_.x + xx_ - 1
        #                 y_ = dot_.y + yy_ - 1
        #
        #                 try:
        #                     # dot_count = Dot(x_, y_)
        #                     # self.shots.remove(dot_count)    # почему то не работает
        #                     for i in range(len(self.shots)):
        #                         if self.shots[i].x == x_ and self.shots[i].y == y_:
        #                             self.shots.pop(i)
        #                             break
        #                 except:
        #                     print('чтото не так')
        #                     continue

        return res


class AI(Player):
    def ask(self):
        resultat = {"dot": None, "error": ""}

        x = random.randint(0, self.enemy_board.max_x - 1)
        y = random.randint(0, self.enemy_board.max_y - 1)
        resultat['dot'] = Dot(x, y)

        # shot = random.choice(self.shots)
        # resultat['dot'] = shot

        return resultat


class User(Player):
    pass
