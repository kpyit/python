

def reverse(text):
    return text[::-1]
def is_palindrome(text):
    return text == reverse(text)

# something = input('Введите текст: ')
# if (is_palindrome(something)):
#     print("Да, это палиндром")
# else:
#     print("Нет, это не палиндром")


poem = '''\
Программировать весело.
Если работа скучна,
Чтобы придать ей весёлый тон -
используй Python!
'''
f = open('poem.txt', 'w') # открываем для записи (writing)
f.write(poem) # записываем текст в файл
f.close() # закрываем файл
f = open('poem.txt') # если не указан режим, по умолчанию подразумевается
# режим чтения ('r'eading)
while True:
    line = f.readline()
    if len(line) == 0: # Нулевая длина обозначает конец файла (EOF)
        break
    print(line, end='')
f.close() # закрываем файл


#библиотека позволяет любой обьект записать в файл и потом его считать обратно

import pickle
# имя файла, в котором мы сохраним объект
shoplistfile = 'shoplist.data'
# список покупок
shoplist = ['яблоки', 'манго', 'морковь']
# Запись в файл
f = open(shoplistfile, 'wb')
pickle.dump(shoplist, f) # помещаем объект в файл  - Этот процесс называется «консервацией» («pickling»)
f.close()
del shoplist # уничтожаем переменную shoplist
# Считываем из хранилища
f = open(shoplistfile, 'rb') #
storedlist = pickle.load(f) # загружаем объект из файла в файле выглядит как ересь - Этот процесс называется «расконсервацией» («unpickling»).
print(storedlist)

######################################################################################################################

try:
    text = input('Введите что-нибудь --> ')
except EOFError:# Нажмите ctrl-d
    print('Ну зачем вы сделали мне EOF?')
except KeyboardInterrupt:# Нажмите ctrl-c
    print('Вы отменили операцию.')
else:
    print('Вы ввели {0}'.format(text))

#способ прервать программу с помощью своего прерывания

class ShortInputException(Exception):
    '''Пользовательский класс исключения.'''
def __init__(self, length, atleast):
    Exception.__init__(self)
    self.length = length
    self.atleast = atleast

try:
    text = input('Введите что-нибудь --> ')
    if len(text) < 3:
        raise ShortInputException(len(text), 3)
# Здесь может происходить обычная работа
except EOFError:
    print('Ну зачем вы сделали мне EOF?')
except ShortInputException as ex:
    print('ShortInputException: Длина введённой строки -- {0}; \
ожидалось, как минимум, {1}'.format(ex.length, ex.atleast))
else:
    print('Не было исключений.')

#########Try .. Finally

import time
try:
    f = open('poem.txt')
    while True: # наш обычный способ читать файлы
        line = f.readline()
        if len(line) == 0:
            break
        print(line, end='')
        time.sleep(2) # Пусть подождёт некоторое время

except KeyboardInterrupt:
    print('!! Вы отменили чтение файла.')
finally:
    f.close()
    print('(Очистка: Закрытие файла)')


#with  as  обертка по типу - try

#обычная запись
l = [str(i)+str(i-1) for i in range(20)]
f = open('text.txt', 'w')
for index in l:
    f.write(index + '\n')
f.close()

#запись с обработчиком  ошибок 
l = [str(i)+str(i-1) for i in range(20)]
with open('text.txt', 'w') as f:
    for index in l:
        f.write(index + '\n')
#тут как бы выполняется finally: f.close() #ну или закрытие любого ресурса

######################################################################################################################

import sys, warnings
if sys.version_info[0] < 3: # (3, 0, 0, 'beta', 2)
    warnings.warn("Для выполнения этой программы необходима как минимум \
        версия Python 3.0",
        RuntimeWarning)
else:
    print('Нормальное продолжение')

print(sys.version_info)

##############


import os, platform, logging
# огромный кусок отвечающий просто за выбор пути логирования для разных платформ
if platform.platform().startswith('Windows'):
    logging_file = os.path.join(os.getenv('HOMEDRIVE'), \
    os.getenv('HOMEPATH'), \
    'test.log')
else:
    logging_file = os.path.join(os.getenv('HOME'), 'test.log')
    print("Сохраняем лог в", logging_file)


print("Сохраняем лог в", logging_file)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s : %(levelname)s : %(message)s',
    filename = logging_file,
    filemode = 'w',
)
logging.debug("Начало программы")
logging.info("Какие-то действия")
logging.warning("Программа умирает")

######################################################################################################################
#ПЕРЕДАЧА КОРТЕЖАМИ  СРАЗУ НЕСКОЛЬКИМ ПЕРЕМЕННЫМ
def get_error_details():
    return (2, 'описание ошибки No2')

errnum, errstr = get_error_details() # СРАЗУ 2 ПЕРЕМЕННЫМ ИДЕТ ПЕРЕДАЧА
#errnum 2   errstr 'описание ошибки No2'
# Обратите внимание, что использование выражения “a, b = <некоторое выражение>”
# интерпретирует результат как кортеж из двух значений.
# Чтобы интерпретировать результат как “(a, <всё остальное>)”, нужно просто поставить
# звёздочку, как это делалось для параметров функций:
# a, *b = [1, 2, 3, 4]
#a 1
#b [2, 3, 4]
#######################################################
#ЛЯМБДЫ
points = [ { 'x' : 2, 'y' : 3 }, { 'x' : 4, 'y' : 1 } ]
points.sort(key=lambda i : i['y'])# СОРТИРОВКА ПО ПОЛЮ С ПОМОЩЬЮ ЛЯМБДЫ
print(points)
#######################################################
#Генераторы списков
listone = [2, 3, 4]
listtwo = [2*i for i in listone if i > 2] # ГЕНЕРАЦИЯ СПИСКА ПО УСЛОВИЮ ИЗ ДРУГОГО СПИСКА!
print(listtwo)

#######################################################
def powersum(power, *args):#1 АРГУМЕНТ 1 ЗНАЧЕНИЕ 2 СО * ВСЕ ОСТАЛЬНЫЕ ПЕРЕДАННЫЕ ПАРАМЕТРЫ
    '''Возвращает сумму аргументов, возведённых в указанную степень.'''
    total = 0
    for i in args:
        total += pow(i, power)
        return total

#powersum(2, 3, 4)
#######################################################
#ЗАПУСК ДИНАМИЧЕСКИ СФОРМИРОВАННОГО ФАЙЛА С КОМАНДАМИ ИЛИ ТЕКСТА ПРОСТО
exec('print("Здравствуй, Мир!")')
eval('2*3')
#######################################################
#Оператор assert
mylist = ['item']
assert len(mylist) >= 1
mylist.pop()
#РЕКОМЕНДУЮТ НЕ ИСПОЛЬЗОВАТЬ




#######################################################
#Необрабатываемые строки
#ТУПО ТЕКСТ В ПАМЯТИ НЕ ПРЕВРАЩЕННЫЙ В МАССИВ ПОЭТОМУ ЕГО НЕ ОБОЙТИ СОЗДАЕТСЯ С ПОМОЩЬЮ r
r"Перевод строки обозначается \n"













