import sys
import warnings

if sys.version_info[0] < 3:  # (3, 0, 0, 'beta', 2)
    warnings.warn("Для выполнения этой программы необходима как минимум \
        версия Python 3.0",
                  RuntimeWarning)

__version__ = '0.1'



import os.path
from os.path import exists
import shutil

import re
import json
import sqlite3 as sql



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




class sqlite_database():
    def __init__(self) -> None:
        # коннектимся к базе
        # возможно нужна проверка наличия базы
        self.conn_l = sql.connect('configurator_mc34063/res/component.db')  # локальный обьект класса

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
        list_resistors = []
        with self.conn_l:
            list_res = self.conn_l.execute(
               f"SELECT * FROM resistance WHERE e_row = {e_row}")
            for row in list_res:
                list_resistors.append(row)
                print(f'строка резистора -',row)
        return list_resistors

    def get_diodes(self) -> list:
            list_resistors = []
            with self.conn_l:
                list_res = self.conn_l.execute(
                f"SELECT * FROM DIODES")
                for row in list_res:
                    list_resistors.append(row)
                    print(f'строка резистора -',row)
            return list_resistors


  

    def import_diodes_in_base(self, list_diodes)->None:
        print('')
        sql_diodes = 'INSERT OR REPLACE INTO DIODES (name_diode, type_of_diode, voltage_max, current_max, body_type, checkpoints, calc_coef, datasheet) values(?, ?, ?, ?, ?, ?, ?, ?)'
        with self.conn_l:
            self.conn_l.executemany(sql_diodes, list_diodes)



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 



if __name__ == '__main__':
    db = sqlite_database()
    # в НАЧАЛЕ СОЗДАНИЕ БАЗ ДАННЫХ
    db.create_tables_base()
    
  
    # print(f'resistor_list = {resistor_list_E96_R_0805}')
    db.insert_resistors(resistor_list_E24_R_0805)
    # db.insert_resistors(resistor_list_E96_R_0805)

    list_diodes = db.import_diodes_info()
    db.import_diodes_in_base(list_diodes)
    db.copy_new_datasheets(list_diodes)


#проверка по графику апроксимации падения напряжения
# diode_analysis = list_diodes[5]
# db.test_plot_diode_forvard_v(diode_analysis)



   




