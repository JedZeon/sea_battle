class Dot:  # класс точек на поле
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):  # other должен быть списком
        # Проверка есть ли точка в списке
        res = False
        for dot in other:
            if self.x == dot.x and self.y == dot.y:
                res = True
                break
        return res


class Ship:
    def __init__(self, length, start_x, start_y, direction, life):
        self.length = length  # Длина
        self.start_ship = Dot(start_x, start_y)  # Точка, где размещён нос корабля
        self.direction = direction  # Направление вертикальное/горизонтальное
        self.life = life  # Количеством жизней (сколько точек корабля ещё не подбито)
        self.dots = self.set_ship_dots()

    def set_ship_dots(self):  # генерация нового корабля
        ship = []
        for i in range(self.length):
            if self.direction == "vertical":
                ship.append(Dot(self.start_ship.x, self.start_ship.y + i))
            else:
                ship.append(Dot(self.start_ship.x + i, self.start_ship.y))
        return ship

    def get_dots(self):
        return self.dots

