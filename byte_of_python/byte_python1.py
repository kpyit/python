def fuck_order():
    x = 2

    def func_2_level():
        x = 4

        def func_3_level():
            nonlocal x  # захват ближайшего
            x = 12
            print(x)
        func_3_level()
        print(x)

    func_2_level()
    print(x)
# fuck_order()


def pre_valued(a, b=2, c=3):
    print(c)


def total(initial=5, *numbers,  # все что можно собрать в кортеж
          **keywords):  # далее ** все что можно собрать в словать
    # def foo(*args: expression, **kwargs: expression):
    count = initial

    for number in numbers:
        count += number

    for key in keywords:
        count += keywords[key]

    return count

# нельзя просто числа добавдять после словаря
#print(total(10, 1, 2, 3, vegetables=50, fruits=100))


# после кортежа можно определять элементы по ключу доступные
def total(initial=5, *numbers, extra_number):
    count = initial
    for number in numbers:
        count += number
    count += extra_number
    print(count)


#total(10, 1, 2, 3, extra_number=50)
# total(10, 1, 2, 3) # Вызовет ошибку, поскольку мы не указали значение аргумента по умолчанию для 'extra_number'
  
def printMax(x: int = 4, y: int = 4) -> None: # тип указывается для удобства при вызове функции и при этом не идет никакая проверка просто для красоты!
    '''Выводит максимальное из двух чисел.
    Оба значения должны быть целыми числами.'''
    x = int(x)  # конвертируем в целые, если возможно
    y = int(y)
    if x > y:  print(x, 'наибольшее')
    else:  print(y, 'наибольшее')

#printMax(3, 5)
#print(printMax.__doc__)  # тройной ''' после функции это автодокументация!
#print(printMax.__annotations__)


import sys
print('Аргументы командной строки:')
for i in sys.argv:
    print(i)


#import os; print('path=' + os.getcwd())#print('\n\nПеременная PYTHONPATH содержит', sys.path, '\n')

from math import * # импорт всего и сразу можно обращатся без префикса модуля

if __name__ == '__main__':   print('Эта программа запущена сама по себе.')
else:    print('Меня импортировали в другой модуль.')

import fmodule
needed_fmodule_version = 1.0
if(float(fmodule.__version__) < needed_fmodule_version):
    print('Version fmodule too old ', fmodule.__version__, '< ',needed_fmodule_version )
else:
    print('Версия', fmodule.__version__)

#fmodule.sayhi()

# все что определено в модуле и вообще работает с любым обьектом
print(dir(sys))

# списки
my_list = [1,2,3,4,5,[2,4]]
# print(my_list[5][1])
# # кортежи те же списки только константы  (2,) константа или кортеж из 1 элемента
my_typle = (1,2,3,4,5,(2,4))
# constanta = (2,)
# print(my_typle[5][1])
# #Множества set  нет повторений элементов не упорядочены  но можно проверять включение 1 в другое, пересечения
bri = set(['Бразилия', 'Россия', 'Индия'])
# print('Индия' in bri)  True
# print('США' in bri)   False
# bric = bri.copy()
# bric.add('Китай')
# print(bric.issuperset(bri)) True
# bri.remove('Россия')
# print()  bri & bric # OR bri.intersection(bric)
# {'Бразилия', 'Индия'}

#по сути копирование ссылки во вторую переменную
#mylist = shoplist # mylist - лишь ещё одно имя, указывающее на тот же объект!
#mylist = shoplist[:] # создаём копию массива путём полной вырезки 
#del mylist[0] # удаляем первый элемент



# -r 	Recurse the subdirectories
# -o 	Set the output directory         -oC:\Doc:    extract all files to the Doc folder on the C: drive
# -mmt:       multithread the operation (faster)
# 7z a -tzip archive.zip subdir\  просто указывается после архива что сжимать
 
#1 пример программы из книги только заточен по 7z архиватор и это жопа
import os
import time
# 1. Файлы и каталоги, которые необходимо скопировать, собираются в список.
#source = ['"H:\python"', 'H:\CPP\CPP_STRAUPT']
source = 'H:\\python'
# Заметьте, что для имён, содержащих пробелы, необходимо использовать
# двойные кавычки внутри строки.
# 2. Резервные копии должны храниться в основном каталоге резерва.
target_dir = 'H:\\arhive' # Подставьте тот путь, который вы будете использовать.
# 3. Файлы помещаются в zip-архив.
# 4. Текущая дата служит именем подкаталога в основном каталоге
today = f"{target_dir}\\{time.strftime('%Y%m%d')}"
# Текущее время служит именем zip-архива
now = time.strftime('%H%M%S')

#comment.replace(' ', '_')  замена элементов строки

# Создаём каталог, если его ещё нет
if not os.path.exists(today):
    os.mkdir(today) # создание каталога
    print('Каталог успешно создан', today)

#target_name =   time.strftime('%Y%m%d%H%M%S')
# 5. Используем команду "zip" для помещения файлов в zip-архив
_7z_command = "C:\PROGRA~1\\7-Zip\\7z.exe a -t7z -mmt4 -r  {0}\\{1}.7z  {2}\\*".format(today, now,  source)
#C:\PROGRA~1\7-Zip\7z.exe a -t7z -mmt4 -r H:\arhive\20220707220856.7z H:\python\* 
print('_7z_command =',_7z_command)
# Запускаем создание резервной копии
if os.system(_7z_command) == 0:
    print('Резервная копия успешно создана в', target_dir)
else:
    print('Создание резервной копии НЕ УДАЛОСЬ')






