from ship import Dot, Ship
import random


class Board:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.arrea = self.generate_area()  # Двумерный список, в котором хранятся состояния каждой из клеток
        self.print_arrea = []  # готовый список строк для печати
        self.list_ship = []  # Список кораблей доски
        self.hide = False  # информация о том, нужно ли скрывать корабли на доске
        self.number_living_ships = 0  # Количество живых кораблей на доске


    def generate_area(self):
        self.arrea = []
        for j in range(self.max_y):
            line_ = []
            for i in range(self.max_x):
                line_.append("O")
            self.arrea.append(line_)
        return self.arrea

    # ставит корабль на доску (если ставить не получается, выбрасываем исключения)
    def add_ship(self, ship_len):
        direction = random.choice(["vertical", "horizontal"])
        xx = random.randint(0, (self.max_x - ship_len - 1 if direction == "horizontal" else self.max_x - 1))
        yy = random.randint(0, (self.max_y - ship_len - 1 if direction == "vertical" else self.max_y - 1))

        mogno_postavit = True

        for i in range(ship_len):
            try:
                if self.arrea[yy + (i if direction == "vertical" else 0)][
                    xx + (i if direction == "horizontal" else 0)] != "O":
                    mogno_postavit = False
                    raise ValueError("Не получилось")
            except:
                print("Не возможно разместить корабль")

        if mogno_postavit:
            ship_ = Ship(ship_len, xx, yy, direction, ship_len)

            for i in range(ship_len):
                self.arrea[yy + (i if direction == "vertical" else 0)][
                    xx + (i if direction == "horizontal" else 0)] = "■"

            self.list_ship.append(ship_)

            self.contur()

        return mogno_postavit

    # обводит корабль по контуру
    def contur(self):

        ship_ = self.list_ship[-1]

        for dot_ in ship_.dots:
            # print("____")
            y_ = 0
            for yy_ in range(3):
                x_ = 0
                for xx_ in range(3):

                    x_ = dot_.x + xx_ - 1
                    y_ = dot_.y + yy_ - 1

                    # print(x_, y_)

                    if (0 <= x_ < self.max_x and 0 <= y_ < self.max_y) and self.arrea[y_][x_] == "O":  # англ
                        self.arrea[y_][x_] = "О"  # рус

    # готовит список строк для вывода в консоль в зависимости от параметра hide
    def print_board(self):

        self.print_arrea.clear()

        for j in range(self.max_y):
            if j == 0:
                si = "  |"
                for ii in range(1, self.max_x + 1):
                    si = si + f"{ii}|"
                self.print_arrea.append(si)
            str_ = f"{j + 1:2}|"
            for i in range(self.max_x):
                if self.arrea[j][i] == "■" and self.hide:
                    str_ = str_ + "O" + "|"
                else:
                    str_ = str_ + self.arrea[j][i] + "|"

            self.print_arrea.append(str_)

    # для точки (объекта класса Dot) возвращает True, если точка выходит за пределы поля, и False, если не выходит
    def check_out(self, dot_):
        if 0 <= dot_.x < self.max_x and 0 <= dot_.y <= self.max_y:
            return True
        else:
            return False

    # делает выстрел по доске (если есть попытка выстрелить за пределы и в использованную точку, нужно выбрасывать исключения)
    def shot(self, dot):
        res = {"repeat": False, "comment": "", 'alive': 1, 'ship_dot': None}

        try:
            # Проверка выстрела по тем же координатам
            if dot.x < 0 or dot.y < 0:
                raise

            if self.arrea[dot.y][dot.x] == "X" or self.arrea[dot.y][dot.x] == "T":
                res["comment"] = "По этим координатам уже стреляли"
                res["repeat"] = True
                return res

            if self.arrea[dot.y][dot.x] == "■":

                ship_ = self.set_life_ship(dot)
                res["comment"] = f" длина {ship_['ship'].length}: жизнь {ship_['ship'].life}"

                if ship_['ship'].life == 0:
                    res["comment"] = f"Убил, повторный выстрел. Осталось {ship_['alive']} кораблей"
                    res['ship_dot'] = ship_['ship'].get_dots()
                else:
                    res["comment"] = "Попал, повторный выстрел"

                res['alive'] = ship_['alive']
                res["repeat"] = True
                self.arrea[dot.y][dot.x] = "X"
            else:
                res["comment"] = "Мимо"
                self.arrea[dot.y][dot.x] = "T"

            return res

        except:
            res["comment"] = "координаты вне поля"
            res["repeat"] = True
            return res

    def set_life_ship(self, dot_):
        res = {"find_ship": False, "ship": None, 'alive': 0}

        for ship_ in self.list_ship:
            if dot_ == ship_.dots:
                res["ship"] = ship_
                res["find_ship"] = True
                ship_.life -= 1
                break

        for ship_ in self.list_ship:
            if ship_.life > 0:
                res['alive'] += 1

        return res
