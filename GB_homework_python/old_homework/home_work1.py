#!/usr/bin/env python
# Filename: home_work1.py
from homework import *

home = home1.homework_1()

# Сделал по 2 реализации с пользовательским вводом и без по заданию не понятно откуда ввод
home.day_is_weekend_by_number(6)
home.day_is_weekend_by_number(7)
home.day_is_weekend_by_number(1)

home.day_is_weekend_by_number_user()

# 2 бонусных метода
home.current_day_is_weekend()

home.day_is_weekend_by_date(10, 7, 2022)

home.enumeration_predicates()

home.quarter_coordinates()

home.quarter_liable_coordinates()

home.distance_between_2_points()
