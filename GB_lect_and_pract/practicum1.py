# def cube_number_test(x,x_2):
#     invar = x*x
#     if(x*x==x_2):
#         print(f'{x_2} is cube of {x}')
#     else:
#         print(f'{x_2} is not cube of {x}')


# x = int(input('введите число-'))
# x_2 = int(input('введите предполагаемый квадрат-'))
# cube_number_test(x,x_2)

# print('Введите 5 чисел для поика максимума')
# diap =  range(1,6,1)
# int_array = []
# for i in diap:    
#     int_array.append(int(input(f'введите {i} число-')))
# #print(int_array)
# max = int_array[0]
# diap =  range(1,5,1)
# for i in diap:
#     if(max <int_array[i]):
#         max = int_array[i]
# print(f'max in array numbers = {max}')



#x = int(input('введите число-'))
#for i in range(-x,x+1):
#    print(i)

x = int(input('введите число-'))
#if(x%5 == 0 and x%10 == 0) or (x%15 == 0 and not(x%30 ==0)):
if((x%5 == 0 and x%10 == 0 or x%15 == 0) and not(x%30 ==0)):
    print('TRUE')
else:
    print('FALSE')

 