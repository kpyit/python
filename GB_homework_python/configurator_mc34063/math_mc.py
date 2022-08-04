


class math_mc():
    def __init__(self):
        print('math')

        
        
    # значение функции в точке по таблице точек
    def lagranz(self, x,y,t):
        
        z=0
        for j in range(len(y)):
            p1=1
            p2=1
            for i in range(len(x)):
                if i==j:
                    p1=p1*1; p2=p2*1
                else:
                    p1=p1*(t-x[i])
                    p2=p2*(x[j]-x[i])
            z=z+y[j]*p1/p2
        return z

    def table(self,x_, y):
        """
        Получить таблицу интерполяции Ньютона
        : param x_: значение списка x
        : param y: значение списка y
        : return: вернуть таблицу интерполяции
        """
        quotient = [[0] * len(x_) for _ in range(len(x_))]
        for n_ in range(len(x_)):
            quotient[n_][0] = y[n_]
            for i in range(1, len(x_)):
                for j in range(i, len(x_)):
                # j-i определяет диагональные элементы
                    quotient[j][i] = (quotient[j][i - 1] - quotient[j - 1][i - 1]) / (x_[j] - x_[j - i])
        return quotient

    def get_corner(self,result):
        """
        Получить диагональные элементы через таблицу интерполяции
        : param result: результат таблицы интерполяции
        : return: диагональный элемент
        """
        link = []
        for i in range(len(result)):
            link.append(result[i][i])
        return link

 
    def newton(self,data_set, x_p, x_7):
        """
        Результат интерполяции Ньютона
        : param data_set: диагональ решаемой задачи
        : param x_p: входное значение
        : param x_7: исходное значение списка x
        : return: результат интерполяции Ньютона
        """
        result = data_set[0]
        for i in range(1, len(data_set)):
            p = data_set[i]
            for j in range(i):
                p *= (x_p - x_7[j])
            result += p
        return result






##################################################################
# max_current = 2
# forvard_v = db.lagranz(points_x,points_y,max_current)
# print(f'forvard_v  {forvard_v}')

# xnew=np.linspace(np.min(points_x),3.2,100)
# ynew=[db.lagranz(points_x,points_y,i) for i in xnew]
# plt.plot(points_y,points_x,'o',ynew,xnew)
# plt.grid(True)
# plt.show()

##################################################################

# middle =  db.table(points_x, points_y)
# n =  db.get_corner(middle)
# forvard_calc =  db.newton(n, max_current , points_x)
# print(f'forvard_calc {forvard_calc}')

# xnew=np.linspace(np.min(points_x),1.52,100)
# ynew=[db.newton(n,i,points_x) for i in xnew]
# plt.plot(points_y,points_x,'o',ynew,xnew)
# plt.grid(True)
# plt.show()

##################################################################
# cubic_f = interp1d(points_x, points_y, kind='cubic')
# max_current = 0.65
# forvard_v = cubic_f(max_current)
# print(f'forvard_v  {forvard_v}')
# cubic_f = interp1d(points_x, points_y, kind='cubic',axis=0, fill_value="extrapolate")
