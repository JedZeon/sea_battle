from player import User, AI
from board import Board
from ship import Ship


class Game:
    def __init__(self):
        self.max_x = 6
        self.max_y = 6
        self.user = User(self.max_x, self.max_y)
        self.user_board = self.user.my_board
        self.komp = AI(self.max_x, self.max_y)
        self.komp_board = self.komp.my_board

        self.user.enemy_board = self.komp_board
        self.komp.enemy_board = self.user_board

    # генерирует случайную доску
    def random_board(self, board):

        board.list_ship.clear()
        board.generate_area()
        board.number_living_ships = 0

        # Список кораблей по правилам
        list_ship = {3: 1, 2: 2, 1: 4}
        # list_ship = {3: 1}
        kol_ship = 0
        for ship_len in list_ship:
            popitka = 0
            kol_ship = kol_ship + list_ship[ship_len]

            # Расставляем корабли
            while popitka < 1000 and list_ship[ship_len] > 0:
                popitka += 1

                # Добавим кораблик
                if board.add_ship(ship_len):
                    list_ship[ship_len] -= 1
                    board.number_living_ships += 1

        if kol_ship != len(board.list_ship):
            print("не удачное поле")
            self.random_board(board)
        else:   # При подготовке поля использован русский символ О, исправляем
            for y in range(self.max_y):
                for x in range(self.max_x):
                    if self.user_board.arrea[y][x] == "О":    # рус
                        self.user_board.arrea[y][x] == "O"    # eng
                    if self.komp_board.arrea[y][x] == "О":    # рус
                        self.komp_board.arrea[y][x] == "O"    # eng

    def greet(self):
        print("-------------------------------")
        print("          Морской бой")
        print("-------------------------------")
        print("Приветствую 'Игрок' ")
        print("Правила игры: На картах игрока и компьютера произвольно размещаются корабли, ")
        print("Игрок вводит координаты выстрела по карте соперника. Если у врага с этими координатами имеется")
        print("'корабль', то корабль или его палуба убивается, попавший делает еще один ход. ")
        print(
            "Цель игрока: первым убить все игровые 'корабли' врага. Вводить координаты требуется числами в формате XY")
        print("1 корабль на 3 клетки, 2 корабля на 2 клетки, 4 корабля на одну клетку")
        print("Расстановка автоматическая, случайная.")
        print("Буквой X помечаются подбитые корабли, буквой T — промахи.")
        input("Продолжить (enter)? ")

    def loop(self):
        hod = True  # True - ход игрока, False - ход компьютера

        # Расстановка кораблей
        self.random_board(self.user_board)
        self.random_board(self.komp_board)

        comment_user, comment_komp = "мои корабли             поле компа", ""
        dubl_comment = ""

        while True:
            print("\n" * 20)

            try:
                # печать поля
                self.user_board.print_board()
                self.komp_board.hide = True
                self.komp_board.print_board()

                for j in range(len(self.user_board.print_arrea)):
                    print(self.user_board.print_arrea[j], "    ", self.komp_board.print_arrea[j])

                print(comment_komp)
                print(comment_user)

                # запрос выстрела
                if hod:
                    res_shot_ = self.user.move()
                    comment_user = "Игрок: " + dubl_comment + res_shot_["comment"]
                else:
                    res_shot_ = self.komp.move()
                    comment_komp = "Компьютер: " + dubl_comment + res_shot_["comment"]


                if res_shot_["alive"] == 0:
                    print(f"{'Поздравляем победил Игрок' if hod else 'Вы проиграли, победил Компьютер'}: ")
                    break

                # comment = f"{'Игрок' if hod else 'Компьютер'}: " + res_shot_["comment"]
                if not res_shot_["double_shot"]:
                    hod = not hod
                    dubl_comment = ""
                else:
                    dubl_comment = dubl_comment + res_shot_["comment"] + ("" if dubl_comment != "" else ", ")

                # if len(dubl_comment) > 30:
                #     dubl_comment = dubl_comment[:-30]
            except:
                print("Что то, не так.")

    def start(self):
        self.greet()
        self.loop()


game = Game()
game.start()
