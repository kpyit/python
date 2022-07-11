class Robot:
    '''Представляет робота с именем.'''
# Переменная класса, содержащая количество роботов
    population = 0

    __privatevar = 3  # c __ начинаются приватные переменные недоступные снаружи класса

    def __init__(self, name):
        #!!!! self.population = 0 спрячет глобальную переменную класса population!!!!!
        '''Инициализация данных.'''
        self.name = name
        print('(Инициализация {0})'.format(self.name))
# При создании этой личности, робот добавляется
# к переменной 'population'
        Robot.population += 1

    def __del__(self):
        '''Я умираю.'''
        print('{0} уничтожается!'.format(self.name))
        Robot.population -= 1
        if Robot.population == 0:
            print('{0} был последним.'.format(self.name))
        else:
            print('Осталось {0:d} работающих роботов.'.format(
                Robot.population))

    def sayHi(self):
        '''Приветствие робота.
        Да, они это могут.'''
        print('Приветствую! Мои хозяева называют меня {0}.'.format(self.name))

#    @staticmethod  ДЕКОРАТОР делает то же что и -  howMany = staticmethod(howMany)
    def howMany():
        '''Выводит численность роботов.'''
        print('У нас {0:d} роботов.'.format(Robot.population))

    # ОБЩАЯ ПЕРЕМЕННАЯ КЛАССА В КОТОРУЮ ПЕРЕДАЮТ ФУНКЦИЯ
    howMany = staticmethod(howMany)


droid1 = Robot('R2-D2')
droid1.sayHi()
Robot.howMany()

droid2 = Robot('C-3PO')
droid2.sayHi()
Robot.howMany()
print("\nЗдесь роботы могут проделать какую-то работу.\n")
print("Роботы закончили свою работу. Давайте уничтожим их.")
del droid1
del droid2
Robot.howMany()



#!/usr/bin/env python
# Filename: inherit_abc.py
from abc import *

class SchoolMember:
#class SchoolMember(metaclass=ABCMeta): #обьявление класса абстрактным чтобы нельзя было  создать экземпляр с помощью спец класса из модуля
    '''Представляет любого человека в школе.'''

    def __init__(self, name, age):
        self.name = name
        self.age = age
        print('(Создан SchoolMember: {0})'.format(self.name))

#    @abstractmethod декоратор делающий метод виртуальным и не позволяет наследникам не переопределять
    def tell(self):
        '''Вывести информацию.'''
        print('Имя:"{0}" Возраст:"{1}"'.format(self.name, self.age), end=" ")


class Teacher(SchoolMember):
    '''Представляет преподавателя.'''

    def __init__(self, name, age, salary):
        SchoolMember.__init__(self, name, age)#конструктор родителя вручную вызывается
        self.salary = salary
        print('(Создан Teacher: {0})'.format(self.name))

    def tell(self):
        SchoolMember.tell(self)
        print('Зарплата: "{0:d}"'.format(self.salary))

class Student(SchoolMember):
    '''Представляет студента.'''

    def __init__(self, name, age, marks):
        SchoolMember.__init__(self, name, age)
        self.marks = marks
        print('(Создан Student: {0})'.format(self.name))

    def tell(self):
        SchoolMember.tell(self)
        print('Оценки: "{0:d}"'.format(self.marks))


t = Teacher('Mrs. Shrividya', 40, 30000)
s = Student('Swaroop', 25, 75)
print()  # печатает пустую строку
members = [t, s]
for member in members:# работает как вирбуальный метод нет своего использует родителя метод
    member.tell()  # работает как для преподавателя, так и для студента
