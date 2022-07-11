from cmath import sqrt
from random import random
from random import randrange
import sys
import warnings
if sys.version_info[0] < 3:  # (3, 0, 0, 'beta', 2)
    warnings.warn("Для выполнения этой программы необходима как минимум \
        версия Python 3.0",
                  RuntimeWarning)

import datetime


__version__ = '0.1'


'''
    Напишите программу, которая принимает на вход вещественное число и показывает сумму его цифр.
    Пример:
- 6782 -> 23
- 0,56 -> 11

    Напишите программу, которая принимает на вход число N и выдает набор произведений чисел от 1 до N.
    Пример:
- пусть N = 4, тогда [ 1, 2, 6, 24 ] (1, 1*2, 1*2*3, 1*2*3*4)
рекурсия

    Задайте список из n чисел последовательности $(1+\frac 1 n)^n$ и выведите на экран их сумму.
    Пример:
- Для n = 6: {1: 4, 2: 7, 3: 10, 4: 13, 5: 16, 6: 19}

    Задайте список из N элементов, заполненных числами из промежутка [-N, N]. Найдите произведение элементов на указанных позициях. Позиции хранятся в файле file.txt в одной строке одно число.

    реализуйте алгоритм перемешивания списка
'''

# Напишите программу, которая принимает на вход вещественное число и показывает сумму его цифр.


def summ_numbers_in_str() -> None:
    try:
        raw_float_str = input(r'Введите вещественное число : ')
    except EOFError:
        print(r'Прервано пользователем EOF')
    except KeyboardInterrupt:
        print(r'Вы отменили операцию.')
    except ValueError:
        print(r'отсутствует либо некорректный ввод.')
    else:
        str_numbers = raw_float_str.translate({ord(c): None for c in ".,_ "})
        print(f'"{str_numbers}"')
        summ = 0
        for number in str_numbers:
            summ += int(number)
        print(f"сумма цифр числа {raw_float_str} = {summ}")


#   Напишите программу, которая принимает на вход число N и выдает набор произведений чисел от 1 до N.
#    Пример:
#    - пусть N = 4, тогда [ 1, 2, 6, 24 ] (1, 1*2, 1*2*3, 1*2*3*4)
#        рекурсия

def factorial_linear() -> None:
    try:
        int_str = input(r'Введите число для расчета факториала : ')
    except EOFError:
        print(r'Прервано пользователем EOF')
    except KeyboardInterrupt:
        print(r'Вы отменили операцию.')
    else:
        if int_str.isdigit():
            int_factiorial = int(int_str)
        else:
            print(r'Вы ввели не число установлено по умолчанию 17.')
            int_factiorial = 17

        str_output_vals = "[ 1"
        str_mustiplay_last = "1"
        str_output_multiplay = "( 1"
        current_val_factorial = 1
        # print(f'int_factiorial = {int_factiorial}')
        int_factiorial
        if(int_factiorial == 1):
            print(
                f" {int_factiorial}! {str_output_vals} ]  {str_output_multiplay} )")
        else:
            for i in range(2, int_factiorial+1):
                current_val_factorial *= i
                str_output_vals = str_output_vals + \
                    r', ' + str(current_val_factorial)
                str_mustiplay_last += r'*'+str(current_val_factorial)
                str_output_multiplay += r', ' + str_mustiplay_last
        print(f" {int_factiorial}! {str_output_vals} ]  {str_output_multiplay} )")


def factorial_recursive() -> None:
    try:
        int_str = input(r'Введите число для расчета факториала : ')
    except EOFError:
        print(r'Прервано пользователем EOF')
    except KeyboardInterrupt:
        print(r'Вы отменили операцию.')
    else:
        if int_str.isdigit():
            int_factiorial = int(int_str)
        else:
            print(r'Вы ввели не число установлено по умолчанию 17.')
            int_factiorial = 17

        def req_factorial(val_factorial: int) -> int:
            if(val_factorial != 1):
                return val_factorial*req_factorial(val_factorial-1)
            else:
                return 1

        current_val_factorial = req_factorial(int_factiorial)

        print(f" {int_factiorial}!  = {current_val_factorial}  ")


#    Задайте список из n чисел последовательности $(1+\frac 1 n)^n$ и выведите на экран их сумму.
#    Пример:  - Для n = 6: {1: 4, 2: 7, 3: 10, 4: 13, 5: 16, 6: 19}

def row_sum_counter() -> None:
    try:
        int_str = input(r'Введите число для рачета суммы ряда : ')
    except EOFError:
        print(r'Прервано пользователем EOF')
    except KeyboardInterrupt:
        print(r'Вы отменили операцию.')
    else:
        if int_str.isdigit():
            row_elements = int(int_str)
        else:
            print(r'Вы ввели не число установлено по умолчанию 10.')
            row_elements = 17

        current_summ = 0
        dict_row = {}

        for i in range(1, row_elements+1):
            current_row_item = (1+1/i)**i
            current_summ += current_row_item
            dict_row.update({i: current_row_item})

        dict_row_str = ', '.join(
            [f'{key}: {value:2.2f}' for key, value in dict_row.items()])

        print(
            f"Для n = {int_str}: ( {dict_row_str} ) сумма = {current_summ:2.2f}")


# Задайте список из N элементов, заполненных числами из промежутка [-N, N]. Найдите произведение элементов на указанных позициях. Позиции хранятся в файле file.txt в одной строке одно число.
# 1 задача создать файл с рандомными числами позиций в списке количество не указано пускай будет случайное от 0 до 10
# 2 создать список из рандомных элементов диапозона и проивести произведение

def list_multipler() -> None:
    try:
        int_str = input(r'Введите размер списка для генерации : ')
    except EOFError:
        print(r'Прервано пользователем EOF')
    except KeyboardInterrupt:
        print(r'Вы отменили операцию.')
    else:
        if int_str.isdigit():
            list_elements = int(int_str)
        else:
            print(r'Вы ввели не число установлено по умолчанию 10.')
            list_elements = 100

        if(list_elements == 0):
            print(r'произведение элементов пустого списка = 0')

        # https://docs.python.org/3/library/random.html
        count_rows_positions = randrange(10)
        # print(f'count_rows_positions = {count_rows_positions}')

        with open('file.txt', 'w') as f:
            for index in range(count_rows_positions):
                f.write(str(randrange(list_elements)) + '\n')

        list_n_size = []
        i = 0
        for i in range(list_elements):
            list_n_size.append(randrange(-list_elements, list_elements+1))

        print(f'список из n элементов= {list_n_size}')

        list_position_mult_elements = []

        with open('file.txt') as f:
            while True:
                line = f.readline()
                if len(line) != 0:
                    list_position_mult_elements.append(int(line))
                else:
                    break

        print(
            f'список элементов для перемножения = {list_position_mult_elements}')

        mult = 1
        for position_el in list_position_mult_elements:
            mult *= list_n_size[position_el]

        print(f'произведение элементов = {mult}')


# реализуйте алгоритм перемешивания списка
# аналог random.sample

def shuffle_list(list_to_reorder: list) -> list:
    # print('list_to_reorder.count '+str(len(list_to_reorder)))
    new_list = []
    for i in range(len(list_to_reorder)):
        id_next = randrange(len(list_to_reorder))
        new_list.append(list_to_reorder.pop(id_next))
    print(f'перемешанный список {new_list}')



