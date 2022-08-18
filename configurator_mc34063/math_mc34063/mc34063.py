import sys
import warnings

if sys.version_info[0] < 3:  # (3, 0, 0, 'beta', 2)
    warnings.warn("Для выполнения этой программы необходима как минимум \
        версия Python 3.0",
                  RuntimeWarning)

__version__ = '0.1'
 
from PyQt5 import QtWidgets, uic, QtWebEngineWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QBrush, QPainter, QPen, QPixmap, QPolygonF,QImage

import numpy as np
import json
import matplotlib.pyplot as plt

# Ряд Е6
RES_E6 = 0
# Ряд Е12
RES_E12 = 1
# Ряд Е24 БАЗОВЫЙ ДЛЯ РАСЧЕТОВ
RES_E24 = 2
# Ряд Е48
RES_E48 = 3
# Ряд Е96 ПОВЫШЕННОЙ ТОЧНОСТИ
RES_E96 = 4

#Типоразмеры резисторов
R_0402 = 1
R_0603 = 2
R_0805 = 3
R_1206 = 4
R_1210 = 5
R_2010 = 6
R_2512 = 7
   
# ИСПОЛЬЗУЕМЫЙ СПИСОК ПО УМОЛЧАНИЮ
DEFAULT_LIST = 1
USER_LIST = 2


class math_mc34063():

    def print_formuls(self, ui) -> None:
        '''выводит формулы в dc dc погнижающий '''
        page_header = r'<html><head><script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script></head><body>'
        page_created = r'''<p><mathjax style="font-size:2.0em">
            <p>Выходное напряжение \(  V_{out} = V_{in} ( \% t_{on}) \; or \; V_{out} = V_{in}({t_{on} \over t_{on} + t_{off}}) \qquad  \)</p>
            <p> Пиковый ток \( I_L = \left({V_{in} - V_{sat} - V_{out} \over L } \right) t \) </p>
            <p> Ток через индуктивность \( I_L =I_{L(pk)} - \left({V_{out}+ V_F \over L}\right)t \)  где \(V_F \) падение на диоде </p>
            <p> Cоотношение времен работы режимов ключа \( \left({Vin - Vsat - Vout \over L}\right)t_{on}  = \left({V_{out} + V_F \over L}\right) t_{off} \)</p>
            <p> \( {t_{on}\over t_{off}} =  {V_{out} + V_F \over V_{in} - V_{sat} - V_{out}} \) </p>
            <p> Отношение пикового тока к среднему \( \left({I_{L(pk)}\over 2} \right) t_{on}  + \left({I_{L(pk)}\over 2} \right)  t_{off}  = (I_{out}t_{on}) + (I_{out} t_{off}) \)</p>
            <p> \({I_{L(pk)}(t_{on} + t_{off}) \over 2}  =  I_{out} (t_{on} + t_{off}) \)</p>
            <p> \(I_{L(pk)} = 2 I_{out} \)</p>
            <p> Емкость частотозадающая  \( CT = I_{chg(min)} \left({\Delta t  \over \Delta V}\right) =  20 \times 10^−6 \left({t_{on}\over 0.5}\right) = 4.0 \times 10^−5 t_{on} \)</p>
            <p> Минимальная рабочая частота \(  f_{min} =  { 1 \over t_{on(max)} + t_{off} } \) </p>
            <p>Пульсация выходного напряжения \( V_{ripple(p−p)} = {I_{pk}(t_{on}+t_{off}) \over 8 C_o}\) где \( C_o \) выходная емкость </p>
            </mathjax>'''
        # <p> Пиковый ток \( I_L = \left({V_{in} - V_{sat} - V_{out} \over L } \right) t \) </p>\
        #page_created = ''
        page_footer = r'</body></html>'

        page = page_header+page_created+page_footer
        # QWebEngineView
        ui.webWidget.setHtml(page)





    def generate_E_row_resistor_nom(self, e_row: int) -> list:
        # e48 e96 полностью совпадает
        # ЛОГАРИФМИЧЕСКИЙ РЯД НЕ РОВНЫЙ ПОЭТОМУ ДЛЯ 24 И НИЖЕ ТАБЛИЧНЫЙ МЕТОД
        E24_row = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7,
                   3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]

        list_E_row = [6, 12, 24, 48, 96]
        E_row_round = [1, 1, 1, 2, 2]
        gen_E_row_resistors = []

        if list_E_row[e_row] < 48:
            for n in range(0, list_E_row[RES_E24], int(24/list_E_row[e_row])):
                # print(f'n {n}')
                gen_E_row_resistors.append(E24_row[n])
        else:
            for n in range(0, list_E_row[e_row]):
                # print(10**(n/list_E_row[e_row]))
                # print(round(10.0**(n/list_E_row[e_row]), E_row_round[e_row]))
                gen_E_row_resistors.append(round(10**(n/list_E_row[e_row]), E_row_round[e_row]))

        # print(f'gen_E_row_resistors = {gen_E_row_resistors}')
        return gen_E_row_resistors



    def generate_list_resistors(self, e_row: int, r_dim:int) -> list:
        ''' генерирует список резисторов с типоразмерами и соотв. параметрами
        '''
        # ряды номиналов 
        dimension_resistor = ['0201','0402','0603','0805','1206','1210','2010','2512']
        # ряды рассеиваемой мощности
        max_power_resistor = [0.05,0.062,0.10,0.10,0.125,0.25,0.50,0.75,1.0]
        # ряд максимального допустимого напряжения
        max_v_resistor = [15, 50, 50, 150, 200, 200, 200]
        list_nominals = self.generate_E_row_resistor_nom(e_row)

        gen_E_row_dim_resistor = []
        for resistir_nom in list_nominals:
            # sql_resistors = 'INSERT INTO RESISTORS (resistance, e_row, device_dissipation, resistor_max_v, body_version, collection_owner)'
            gen_E_row_dim_resistor.append([resistir_nom, e_row, max_power_resistor[r_dim],max_v_resistor[r_dim],dimension_resistor[r_dim],DEFAULT_LIST])

        return gen_E_row_dim_resistor

 

    def test_plot_diode_forvard_v(self,diode_analysis)-> None:
        print(f'list_diodes[0][5] {diode_analysis[5]}')
        points_x_y = json.loads(diode_analysis[5])
        print(f'points_x_y {points_x_y}')
        points_x = points_x_y[0]
        points_y = points_x_y[1]
        max_current = diode_analysis[3]/1000

        coef = np.polyfit(points_x, points_y, 3)
        print(f'coef {coef}')# кэфф совпадают график нет https://planetcalc.ru/5992/
        # https://docs.scipy.org/doc/scipy/tutorial/interpolate.html
        cubic_regression = np.poly1d(coef)#https://www.w3schools.com/python/python_ml_polynomial_regression.asp
        print(f' cubic_regression.order {cubic_regression.order}')

        test_current = 0.65
        forvard_v = cubic_regression(test_current)
        print(f'forvard_v  {forvard_v}')

        xnew=np.linspace(np.min(points_x),max_current,100)
        ynew=cubic_regression(xnew)

        plt.plot(points_y,points_x,'o',ynew,xnew)
        plt.grid(True)
        plt.show()


    def calc_coef_regression(self,json_points:str)->list:
        '''архивную строку json точек превращает в коэф регрессии json'''
        print(f'json_points {json_points}')
        points_x_y = json.loads(json_points)
        print(f'points_x_y {points_x_y}')
        points_x = points_x_y[0]
        points_y = points_x_y[1]
        coef = list(np.polyfit(points_x, points_y, 3))
        print(f'coef {coef}')
        return coef


    def calc_v_drop_by_current(self,coef:list,test_current:float)->float:
        '''расчет падения напряжения по току'''
        print(f'coef {coef}')# кэфф совпадают график нет https://planetcalc.ru/5992/
        # https://docs.scipy.org/doc/scipy/tutorial/interpolate.html
        cubic_regression = np.poly1d(coef)#https://www.w3schools.com/python/python_ml_polynomial_regression.asp
        print(f' cubic_regression.order {cubic_regression.order}')
        print(f' test_current {test_current}')
        
        forvard_v = cubic_regression(test_current)
        print(f'forvard_v  {forvard_v}')

        return forvard_v

# Расчеты в математике

####################################################################################################
    
    #математика расчета
    # Вводные
    # Vout = 5.0 V
    # Iout = 50 mA
    # fmin = 50 kHz
    # Vin(min) = 24 V − 10% or 21.6 V
    # Vripple(p−p) = 0.5% V_out or 25mV(p−p)

    def init_params_back(self) -> None:
        self.Vout = 5.0
        self.Iout = 50 #mA а амперы прийдется приводить к милиамперам
        self.fmin = 50 #kHz частота только в килогерцах от 10 до 100 границы
        self.Vin = 24  #тест на напряжение от 3.0 V to 40 V
        self.delta_v_percent = 10  #отклонение напряжения в меньшую сторону
        self.Vin_min = self.Vin*(1.0-self.delta_v_percent/100.0)
        print(f"self.Vin_min {self.Vin_min} V")
        # допуск по пульсациям есть нижняя граница за счет компоратора
        self.Vripple_p_p_percent = 0.5 # %
        self.Vripple_p_p = self.Vout*(1.0-self.Vripple_p_p_percent/100.0) #= 0.025 # 25mV(p−p)
        print(f"self.Vripple_p_p {self.Vripple_p_p} V")
        #возможно на диоде?
        self.V_F = 0.8
        #V_F падение на ключе
        self.V_sat = 0.8
        

    # расчет времени открытого и закрытого диода(кочено при предельной загрузке)
    # t_on/t_off  = (Vout + V_F)/(V_in(min) - V_sat - V_out)
    # = (5.0 + 0.8)/(21.6 - 0.8 - 5.0) = 0.37
    def calc_t_on_t_off(self) -> None:
       self.t_on_div_t_off  = (self.Vout + self.V_F)/(self.Vin_min - self.V_sat - self.Vout)
       print(f"self.t_on_div_t_off {self.t_on_div_t_off:3.3f}")
 
    # Тоесть микро секунды а частоту можно задавать в килогерцах сразу.
    # ton(max) + toff   = 1/f_min = 1/(50*10^3) = 20 us на такт
    def calc_t_on_sum_t_off( self ) -> None:
        self.t_on_sum_t_off  = 1/( self.fmin*10**3 )
        print( f"self.t_on_sum_t_off {self.t_on_sum_t_off:3.3f} us" )

    # toff = (ton(max) + toff)/(ton/toff + 1)
    # = 20 * 10**− 6/(0.37 +1 )
    def calc_t_off(self):
        self.t_off  = self.t_on_sum_t_off/(1+ self.t_on_div_t_off)
        print( f"self.t_off {self.t_off:3.3f} us" )

    # ton(max) + toff = 20 us
    # ton(max) = 20 us - 14.6 us =  5.4 us        
    def calc_t_on_max(self):
        self.t_on_max  = self.t_on_sum_t_off-self.calc_t_off
        print( f"self.t_on_max {self.t_on_max:3.3f} us" )
        
    # 4) C_T = 4.0 * 10**− 5* ton
    #  = 4.0 * 10**− 5 (5.4 * 10**− 6) =  216 pF
    def calc_C_t(self):
        self.C_t  =  4.0 * 10**-5 * self.t_on_max
        print( f"self.C_t {self.C_t:3.3f} pF")
        # Ряд конденсаторов формируется просто  http://katod-anod.ru/articles/59
        # 				Ряд Е6 10, 15, 22, 33, 47, 68 каждый следующий номинал +10
        # из него выбирается подходящий

    # 5) ранее расчитанному среднему току
    # Ipk(switch)  = 2*Iout = 2*(50*10−3) = 100_mA
    def calc_I_pk_switch(self):
        self.Ipk_switch  =  2.0 * self.Iout
        print(f"self.Ipk_switch {self.Ipk_switch:3.3f} mA")

    # 6) смотрим разность напряжений между входным и выходным каскадом делим его на пиковый ток и умножаем на время
    # в состоянии заряда  разряд почему-то не удаляем
    # Lmin = ( ( Vin(min) - Vsat - Vout )/Ipk(switch) ) * ton(max) =
    # = (21.6-0.8-5.0 )/100*10**−3 )*5.4*10**−6 =
    # = 853 uH
    def calc_Lmin(self):
        self.Lmin = ( ( self.Vin_min - self.V_sat - self.Vout )/self.Ipk_switch ) * self.t_on_max
        print(f"self.Lmin {self.Lmin:3.3f} uH")

    # 7) Значение резистора ограничения тока, Rsc, может быть определено с помощью текущего уровня Ipk(switch) при Uвх = 24 В(Макс)
    # расчет токаограничивающего резистора
    # Ipk(switch) = ( (Vin - Vsat - Vout)/Lmin)*ton(max) = 
    # = ((24 - 0.8- 5.0)/853*10**-6)* 5.4*10-6 =  115 mA
    def _calc_Ipk_switch_Vmax(self):
        self.Ipk_switch_Vmax = ((self.Vin - self.V_sat - self.Vout)/self.Lmin)*self.t_on_max
        print(f"self.Ipk_switch_Vmax {self.Ipk_switch_Vmax:3.3f} mA")

    # Rsc =  0.33/Ipk(switch)  = 0.33/115*10**−3 = 2.86 Om, use 2.7 из ряда номиналов ближайший меньший
    # тут нужен тест на пиковый ток он не должен быть более 1.5А который якобы выдерживает внутренний в микросхеме
    def calc_Ipk_switch_Vmax(self):
        self._calc_Ipk_switch_Vmax()
        self.Rsc =  0.33/self.Ipk_switch_Vmax
        print(f"self.Rsc {self.Rsc:3.3f} mA")

    # 8) Минимальное значение для идеального конденсатора выходного фильтра
    # Co = (Ipk(switch)*(ton + toff))/(8*Vripple(p-p))
    # = (0.1*(20*10**-6))/8 (25*10**-3) = 10 uF
    def calc_С_output(self):
        # я бы подставил предельный ток а не при минимальном напряжении
        self.C_o = (self.Ipk_switch*(self.t_on + self.t_off))/(8*self.Vripple_p_p)        
        print(f"self.C_o {self.C_o:3.3f} uF")

    # 9) Номинальное выходное напряжение программируется Резисторным делителем R1, R2. Выходное напряжение:
    # V = 1.25(R2/R1 + 1)
    # V_out = V_in(%ton)
    # V_out = V_in(ton/(ton + toff)
    # Ток делителя может достигать 100 мкА без влияния на производительность системы. 
    # При выборе минимальный делитель тока R1 равен: 
    # R1 = 1.25/(100*10**-6) = 12.500 Om
    def calc_R1(self):
        # расчет ужасен
        self.R1 = 1.25/(100*10**-6)
        print(f"self.R1 {self.R1:3.3f} uF")

    # Подставляем приведенное выше уравнение так, чтобы R2 можно было вычислить:
    # R2 = R1*(Vout/1.25 - 1)
    # Если для R1 выбран стандартный резистор 12 кОм с допуском 5%, R2 также будет стандартным значением.
    # R2 = 12*10**3(5.0/1.25-1) = 36 kOm
    def calc_R2(self):
        self.R2 = self.R1*(self.Vout/1.25-1)
        print(f"self.R2 {self.R2:3.3f} uF")



    # # #
    def test_calc_buck(self)->None:
        self.init_params_back()
        self.calc_t_on_t_off()
        self.calc_t_on_sum_t_off()
        self.calc_t_off()
        self.calc_t_on_max()
        self.calc_C_t()
        self.calc_I_pk_switch()
        self.calc_Lmin()
        self._calc_Ipk_switch_Vmax()
        self.calc_С_output()
        self.calc_R1()
        self.calc_R2()

 





# НЕ ИСПОЛЬЗУЕМОЕ ************************************
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

 

if __name__ == '__main__':

    mathematics = math_mc34063() 
    
    resistor_list_E24_R_0805 = mathematics.generate_list_resistors(RES_E24,R_0805)
    # resistor_list_E96_R_0805 = mathematics.generate_list_resistors(RES_E96,R_0805)


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
