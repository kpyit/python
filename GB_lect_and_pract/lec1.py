#efefprint('hell')
a = 14
b = 2#1.34
val = None
#print(a)
#print(b)
#print(val)
#print(type(val))
#val = 23
#print(val)
#print(type(val))
s = "hellooo"
#print(a,'-', b, s) # 
bl = True
#print('{} - {} - {}'.format(a, b, val))#
#print(f'{a} - {b} - {val}')#
#print('{2} - {1} - {0}'.format(a, b, val)) #
list2 = ['1','2','3',1, 2, 3] #можно но плохо несколько типов сразу в списке 
#print('Введите а')
#a = input() //по умолчанию все строки
#print('input b')
#b = float(input())
#print(a*b,b)#можно умножать целое число на строку но нельзя складывать разные типы 
#c = None print(с = a + b)  нельзя прямо в выводе использовать

#c = a/b; print(c) #по умолчанию от деления получаем float
#для целочисленного деления //
#c = a//b; print(c) #тоже float только без десятичной
#c = int(a//b); print(c)
#c = int(a/b); print(c)
c = (a**b); print(c)# если все целое то и получишь целое! иначе float
с = round(a*b,5)# доп параметр сколько знаков после запятой не обрезать
# логические о  перации  и бинарные not and or   & | ^  можно в 1 строке сразу несколько оператов сравнения использовать 
print(2<3>1<5)
x = ["apple", "banana", "cherry"]
y = x # будут ссылаться на 1 и тот же массив поэтому это 1 и тотже обьект по сути проверка ссылки
p = ''' # вот такой извращенный тип комментария
print(x is y) 
if a>b:
    print(b)
elif b==a:
    print('frends') 
else:
    print(a)
#инвертирование числа
original  = 75
inverted = 0
while original != 0:
    inverted = inverted * 10 + (original % 10)
    original //=10
else:
    None
print(inverted)
print(""" gjl
dfdfd""")
enumerad = [1,4,4,4]
for i in enumerad:
    print(i)
r = range(2,40,10)
for i in r:
    print(i)
for i in 'dwdd wd':
    print(i)
text = 'сьешь еще эти булок'
print(len(text)) #
print('ещё' in text)
print(text.isdigit())
print(text.islower())
print(text.replaсe('еще', "ЕЩЕ"))

text = 'сьешь еще эти булок'
help(text.istitle)
print(text[len(text)-1])
print(text[-6])#6 символов от конца
print(text[len(text)-1:])# до конца 
print(text[len(text)-12::2])# выбока с шагом
'''
numb = [1, 2, 3, 4, 5]
ran = range(1, 6)
tuple_t = ('/',23,34,12)# tuple is a collection which is ordered and unchangeable. и допустимы дубликаты
print(type(tuple_t))

myset = {"apple", "banana", "cherry"} #set - неиндекирован неизменяемые члены поч неупорядоченная
#недопустимы дубликаты  можно добавлять и удалять элементы 

thisdict =	{ #словарь упорядочен(с py3.6) индексирован не допускает дубикаты
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964,
  "colors": ["red", "white", "blue"]
}
#print(thisdict["brand"])

numb.append(4)
print(numb)
numb.remove(4) #удалит первое вхождение 4
print(numb)
del numb[0]
print(numb)

# Python Collections (Arrays)   four collection data types
#    List is a collection which is ordered and changeable. Allows duplicate members.
#    Tuple is a collection which is ordered and unchangeable. Allows duplicate members.
#    Set is a collection which is unordered, unchangeable*, and unindexed. No duplicate members.
#    Dictionary is a collection which is ordered** and changeable. No duplicate members.

 

#print(list[1, 2, 3])
#numbers = list(ran) #приведение типа
#vowel_string = 'aeiou'
#print(list(vowel_string))

#initialize tuple
aTuple = (True, 28, 'Tiger')
#tuple to list
aList = list(aTuple)
#print list
print(type(aList))
print(aList)


def func_test(x):
    if x == 1:
        return "dfdf"
    elif x == 2.3:
        return 34
    else:
        return 





