# lambda анонимная функция
# включения генератор новой
# map
# filter
# zip
# enumerate
def even_items(iterable):
    return [v for i, v in enumerate(iterable, start=1) if not i % 2]

numbers1 = [1, 2, 3]
numbers2 = [4, 5, 6]
result = list(map(lambda x, y: x + y, numbers1, numbers2))
 
def fn(x): return x**2


def fn(x): return x**2
print(fn(20))

numbers1 = [1, 2, 3]
numbers2 = [4, 5, 6]
  
result = list(map(lambda x, y: x + y, numbers1, numbers2))

print(result)
 
my_list = [1, 2, 3, 4]
for item in my_list:
    print(fn(item))

# res = list(map(fn, my_list))
res = map(fn, my_list)
mapped_numbers = list(map(lambda x: x * 2 + 3, my_list))
# res = tuple(map(fn, my_list))
print(res)
print(f'mapped_numbers {mapped_numbers}')


# тернарка
def new_f(x): return True if(x > 10) else False
# лямда тернарка
ft = lambda x:  True if(x > 10) else False

my_list = [1, 13, 4, 15]
# res = map(new_f, my_list)
res = list(map(new_f, my_list))
print(res)

mlist = [i for i in range(10) if i>5]
# mlist = (i for i in range(10) if i>5) генератор


for i in range(10):
    if i > 10:
        print(i)
mlist = [print(i) for i in range(10) if i>5]
# забавный ввод
# [input() for i in range(5)]
list2 = [(i,i) for i in range(1,21) if i%2 == 0]
# list2 = [(i,i) for i in range(1,21) if i%2 == 0]
print(f'list2 {list2}')


my_list = list(filter(lambda x:x>5,[123,232,32,4]))