from cmath import sqrt
import sys
import warnings
if sys.version_info[0] < 3:  # (3, 0, 0, 'beta', 2)
    warnings.warn("Для выполнения этой программы необходима как минимум \
        версия Python 3.0",
                  RuntimeWarning)

import datetime


__version__ = '0.1'


class homework_1:
    '''
    Напишите программу, которая принимает на вход цифру, обозначающую день недели, и проверяет, является ли этот день выходным.
    Пример:
    - 6 -> да
    - 7 -> да
    - 1 -> нет

    Напишите программу для. проверки истинности утверждения ¬(X ⋁ Y ⋁ Z) = ¬X ⋀ ¬Y ⋀ ¬Z для всех значений предикат.

    Напишите программу, которая принимает на вход координаты точки (X и Y), причём X ≠ 0 и Y ≠ 0 и выдаёт номер четверти плоскости, в которой находится эта точка (или на какой оси она находится).
    Пример:
    - x=34; y=-30 -> 4
    - x=2; y=4-> 1
    - x=-34; y=-30 -> 3

    Напишите программу, которая по заданному номеру четверти, показывает диапазон возможных координат точек в этой четверти (x и y).

    Напишите программу, которая принимает на вход координаты двух точек и находит расстояние между ними в 2D пространстве.
    Пример:

    - A (3,6); B (2,1) -> 5,09
    - A (7,-5); B (1,-1) -> 7,21
    '''

    def day_is_weekend_by_number(self, number_day_week: int) -> bool:
        if number_day_week > 4:
            print(r'Ура выходной!')
            return True
        else:
            print(r'Надо еще немного поработать')
            return False

    def day_is_weekend_by_number_user(self) -> bool:
        try:
            number_day_week = int(input(r'Введите номер дня недели - ')) % 7
        except EOFError:
            print(r'Прервано пользователем EOF')
        except KeyboardInterrupt:
            print(r'Вы отменили операцию.')
        else:
            print(f'текущий день - {number_day_week}')
            if number_day_week > 4:
                print(r'Ура выходной!')
                return True
            else:
                print(r'Надо еще немного поработать')
                return False


    def current_day_is_weekend(self) -> bool:
        weekday_number = datetime.datetime.today().weekday()
        date = datetime.datetime.today()
        print(f'сегодня {date:%B %d, %Y}')
        if weekday_number > 4:
            print(r'Сегодня выходной!')
            return True
        else:
            print(r'Сегодня не выходной...')
            return False

    def day_is_weekend_by_date(self, day: int, month: int, year: int) -> bool:
        date = datetime.date(year, month, day)
        print(f'дата {date:%B %d, %Y}')
        if date.weekday() < 5:
            print(r'не выходной...')
            return True
        else:
            print(r'выходной!')
            return False

    def enumeration_predicates(self) -> None:
        print(r'¬(X ⋁ Y ⋁ Z) = ¬X ⋀ ¬Y ⋀ ¬Z')
        for X in (True, False):
            for Y in (True, False):
                for Z in (True, False):
                    rez = (not(X or Y or Z)) == (not X and not Y or not Z)
                    # ВЫГЛЯДИТ ЖУТКОЙ СМЕСЬЮ ПОДБИРАЛ ЛУЧШИЙ ИЗ ДОСТУПНЫХ ВАРИАНТОВ ВЫВОДА
                    print('X={4!r:6} Y={1:6} Z={2:6}    ¬({3:d} ⋁ {4:d} ⋁ {5:d}) = ¬{3:d} ⋀ ¬{4:d} ⋀ ¬{5:d} == {6}'.format(
                        X, Y.__repr__(), str(Z), X, Y, Z, rez))

    def quarter_coordinates(self) -> None:
        try:
            coord_X = int(input(r'Введите координату Х = '))
            coord_Y = int(input(r'Введите координату Y = '))
        except EOFError:
            print(r'Прервано пользователем EOF')
        except KeyboardInterrupt:
            print(r'Вы отменили операцию.')
        else:
            if(coord_X > 0 and coord_Y > 0):
                print(
                    f" точка({coord_X},{coord_Y}) лежит в 1 квадранте плоскости")
            elif(coord_X < 0 and coord_Y > 0):
                print(
                    f" точка({coord_X},{coord_Y}) лежит в 2 квадранте плоскости")
            elif(coord_X < 0 and coord_Y < 0):
                print(
                    f" точка({coord_X},{coord_Y}) лежит в 3 квадранте плоскости")
            elif(coord_X > 0 and coord_Y < 0):
                print(
                    f" точка({coord_X},{coord_Y}) лежит в 4 квадранте плоскости")

    # Напишите программу, которая по заданному номеру четверти, показывает диапазон возможных координат точек в этой четверти (x и y).

    def quarter_liable_coordinates(self) -> None:
        try:
            current_quarter = int(input(r'Введите номер квадранта = '))
        except EOFError:
            print(r'Прервано пользователем EOF')
        except KeyboardInterrupt:
            print(r'Вы отменили операцию.')
        else:
            if(current_quarter == 1):
                print(r' X∈(0,INF) Y∈(0,INF)')
            elif(current_quarter == 2):
                print(r' X∈(0,-INF) Y∈(0,INF)')
            elif(current_quarter == 3):
                print(r' X∈(0,-INF) Y∈(0,-INF)')
            elif(current_quarter == 4):
                print(r' X∈(0,INF) Y∈(0,-INF)')
            else:
                print(r' квадрант в данной системе координат отсутсвует ')

    def distance_between_2_points(self) -> None:
        try:
            X_a = float(input(r'Введите X первой точки= '))
            Y_a = float(input(r'Введите Y первой точки= '))
            X_b = float(input(r'Введите X второй точки= '))
            Y_b = float(input(r'Введите Y второй точки= '))
        except EOFError:
            print(r'Прервано пользователем EOF')
        except KeyboardInterrupt:
            print(r'Вы отменили операцию.')
        except ValueError:
            print(r'отсутствует либо некорректный ввод.')
        else:
            distance_AB = ((X_a-X_b)**2+(Y_a-Y_b)**2)**(1/2)
            print(f"Расстояние между точками ({X_a:2.2f}, {Y_a:2.2f}) и ({X_b:2.2f}, {Y_b:2.2f}) равно {distance_AB:2.3f}")


