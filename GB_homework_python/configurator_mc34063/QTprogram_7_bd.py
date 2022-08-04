import os.path
from os.path import exists
import shutil

import re
import json
import sqlite3 as sql

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d



# Введение
# https://medium.com/nuances-of-programming/встроенная-база-данных-python-bb6327b2aab1

# простая программа администрирования базы
# https://dbeaver.io/download/


# КОНСТАНТЫ ТИПОВ ДИОДА
# type_of_diode
D_TYPE_NONE = 0
D_TYPE_PN = 1
D_TYPE_SCHOTTKY = 2
D_TYPE_FIELD_TRANS = 3

# ИЗВЕСТНЫЕ ФИРМЫ ПРОИЗВОДИТЕЛИ
# manufacturer
ON_SEMICONDUCTOR = 1
TEXAS_INSTRUMENTS = 2
VISHAY = 3

# исполнение
TYPE_SMD = 1
TYPE_PIN = 2

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

# Временно пути к вложенным каталогам
PATH_IMPORT = r'GB_homework_python/configurator_mc34063/diodes_import/'
PATH_DATASHEETS = r'GB_homework_python/configurator_mc34063/datasheets/'
FILE_IMPORT_DIODES_TEXT = r'import_diodes.txt'
FILE_IMPORT_DIODES_SVF = r'import_diodes.csv'

POSITION_DATASHEET = 7




class sqlite_database():
    def __init__(self) -> None:
        # коннектимся к базе
        # возможно нужна проверка наличия базы
        self.conn_l = sql.connect('GB_homework_python/configurator_mc34063/component.db')  # локальный обьект класса

    def create_tables_base(self):
        # 3 таблицы конденсаторы и индукторы бы тоже добавить ВОЗМОЖНО ЕЩЕ ТАБЛИЦУ КЛЮЧИ ДОБАВИТЬ И ТУДА ПОЛОЖИТЬ И ПОЛЕВЫЕ И PNP
        #
        # Диоды
        # Название диода      фирма(на всякий)        допустимый ток в мА       допустимое напряжение   тип(pn=1 schottky=2)    ИСПОЛНЕНИЕ SMD/PIN    контрольные точки [1:2 2:3 3:4 4:4]
        # name_diode         # manufacturer            # current_max            # voltage_max           # type_of_diode         # body_type        # checkpoints

        # расчетные коэф по лагражу [1,2,3,4]     МОЩНОСТЬ РАССЕИВАЕМАЯ     приблизительная цена      Даташит
        # calculated coefficients - calc_coef     # device_dissipation      # approx_price            # datasheet

        with self.conn_l:
            self.conn_l.execute("""
                CREATE TABLE if not exists DIODES (
                    id_d INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    name_diode TEXT UNIQUE,
                    type_of_diode INTEGER,
                    current_max INTEGER,
                    voltage_max INTEGER,
                    body_type INTEGER,
                    checkpoints TEXT,
                    calc_coef REAL,
                    device_dissipation REAL,
                    approx_price REAL,
                    datasheet TEXT,
                    manufacturer INTEGER                    
                );
            """)
            # UNIQUE(name_diode)

        # РЕЗИСТОРЫ
        # НОМИНАЛ РЕЗИСТОРА Om        ТОЧНОСТЬ РЕЗИСТОРА(РЯД)      МОЩНОСТЬ РАССЕИВАЕМАЯ     макс_напряжение          ИСПОЛНЕНИЕ SMD/PIN      КОЛЛЕКЦИЯ ВНУТР/ПОЛЬЗОВАТЕЛЬСКАЯ
        # resistance                  #e_row                       resistor_dissipation      resistor_max_v           body_type            collection_owner
        with self.conn_l:
            self.conn_l.execute("""
                CREATE TABLE if not exists RESISTORS (
                    id_r INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    resistance INTEGER,
                    e_row INTEGER,
                    resistor_dissipation REAL,
                    resistor_max_v REAL,
                    body_type TEXT,
                    collection_owner INTEGER
                );
            """)

         # КОНДЕНСАТОРЫ
         # НОМИНАЛ                  ТОЧНОСТЬ                       МАТЕРИАЛ                 ИСПОЛНЕНИЕ SMD/PIN       КОЛЛЕКЦИЯ
 

    def insert_resistors(self, list_resistors) -> None:
        print('insert resistors')
        sql_resistors = 'INSERT INTO RESISTORS (resistance, e_row, resistor_dissipation, resistor_max_v, body_type, collection_owner) values(?, ?, ?, ?, ?, ?)' 
        with self.conn_l:
            self.conn_l.executemany(sql_resistors, list_resistors)





    def get_e_resistors(self, e_row: int) -> list:
        with self.conn_l:
            list_resistors = self.conn_l.execute(
                "SELECT * FROM resistance WHERE e_row = {e_row}")
            # for row in data:
            # print(row)
        return list_resistors


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

    def import_diodes_info(self)->list:
        ''' импортирует перечень диодов с даташитами и расчитывает коэф ур Лагранжа
        '''
        name_type_diodes_shottky = {'шотки','шоттки','schottky'}
        name_type_diodes_semiconductor = {'pn','np','полупроводниковый',''}
        type_mount_sm = {'поверхностный','smd'}
        type_mount_pin = {'штыревой','pin'}
        list_diodes = []

        if(os.path.exists(PATH_IMPORT+FILE_IMPORT_DIODES_TEXT)):
            with open(PATH_IMPORT+FILE_IMPORT_DIODES_TEXT, mode="r", encoding="utf-8") as f:
                for line in f.readlines():
                    if not line.startswith("#"):#
                        diode = []                        
                        line = re.sub(r'(^[ \t\n]+|[ \t\n]+)', '', line, flags=re.M)
                        diode_params = re.split(",", line, flags=re.UNICODE)
                        print(f'line {diode_params} len(line)={len(diode_params)} ')
                        # Имя диода
                        diode.append(diode_params[0])
                        # Тип диода
                        # print(f'list_diodes[1].lower() {diode_params[1].lower()}')
                        if diode_params[1].lower() in name_type_diodes_shottky:
                            diode.append(D_TYPE_SCHOTTKY)
                        else:
                            diode.append(D_TYPE_PN)
                        # допустимое напряжение
                        voltage = re.sub(r'([\D]+)', '', diode_params[2])
                        # print(f'voltage {voltage} ')
                        diode.append(int(voltage))
                        # допустимый ток
                        current = re.sub(r'([\D]+)', '', diode_params[3])
                        # print(f'current {current} ')
                        diode.append(float(current)*1000.0)
                        # тип монтажа
                        if diode_params[4].lower() in type_mount_sm:
                            diode.append(TYPE_SMD)
                        else:
                            diode.append(TYPE_PIN)

                        #генерация коэф по точкам 
                        #Помойму это не по канонам Питона!
                        x_list = [float(x) for id, x in enumerate(diode_params[5:13]) if id%2 == 0]
                        y_list = [float(y) for id, y in enumerate(diode_params[5:13]) if id%2 == 1]
                        diode.append(json.dumps([x_list, y_list]))

                        #пока пустой список но можно сохранять расчетные коэф 
                        diode.append(json.dumps([]))


                        # print(f'datasheet {diode_params[13]}')
                        diode.append(diode_params[13])
                        list_diodes.append(diode)


        print(f'list_diodes {list_diodes}')

        return list_diodes

 
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




    def copy_new_datasheets(self, list_diodes)->None:
        list_datasheets = [x[POSITION_DATASHEET] for x in list_diodes]
        print(f'list_datasheets {list_datasheets}')

        for data in list_datasheets:
            print(f'{exists(PATH_IMPORT+data)} and {not exists(PATH_DATASHEETS+data)}')
            # print(f'{exists(PATH_IMPORT+data) and (not exists(PATH_DATASHEETS+data))}')
            if exists(PATH_IMPORT+data) and (not exists(PATH_DATASHEETS+data)):
                shutil.copyfile(PATH_IMPORT+data, PATH_DATASHEETS+data)
     

    def import_diodes_in_base(self, list_diodes)->None:
        print('')
        sql_diodes = 'INSERT OR REPLACE INTO DIODES (name_diode, type_of_diode, voltage_max, current_max, body_type, checkpoints, calc_coef, datasheet) values(?, ?, ?, ?, ?, ?, ?, ?)'
        with self.conn_l:
            self.conn_l.executemany(sql_diodes, list_diodes)







# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 



db = sqlite_database()

# в НАЧАЛЕ СОЗДАНИЕ БАЗ ДАННЫХ
db.create_tables_base()

resistor_list_E24_R_0805 = db.generate_list_resistors(RES_E24,R_0805)
# resistor_list_E96_R_0805 = db.generate_list_resistors(RES_E96,R_0805)
# print(f'resistor_list = {resistor_list_E96_R_0805}')
db.insert_resistors(resistor_list_E24_R_0805)
# db.insert_resistors(resistor_list_E96_R_0805)

list_diodes = db.import_diodes_info()
db.import_diodes_in_base(list_diodes)
db.copy_new_datasheets(list_diodes)

#проверка по графику апроксимации падения напряжения
# diode_analysis = list_diodes[5]
# db.test_plot_diode_forvard_v(diode_analysis)

   




