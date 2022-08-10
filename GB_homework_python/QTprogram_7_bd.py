import json
import sqlite3 as sql
# Введение
# https://medium.com/nuances-of-programming/встроенная-база-данных-python-bb6327b2aab1

# простая программа администрирования базы
# https://dbeaver.io/download/
conn_l = sql.connect('component.db')


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
        self.conn_l = sql.connect('component.db')  # локальный обьект класса

    def create_tables_base(self):
        # 3 таблицы конденсаторы и индукторы бы тоже добавить ВОЗМОЖНО ЕЩЕ ТАБЛИЦУ КЛЮЧИ ДОБАВИТЬ И ТУДА ПОЛОЖИТЬ И ПОЛЕВЫЕ И PNP
        #
        # Диоды
        # Название диода      фирма(на всякий)        допустимый ток в мА       допустимое напряжение   тип(pn=1 schottky=2)    ИСПОЛНЕНИЕ SMD/PIN    контрольные точки [1:2 2:3 3:4 4:4]
        # name_diode         # manufacturer            # current_max            # voltage_max           # type_of_diode         # body_version        # checkpoints

        # расчетные коэф по лагражу [1,2,3,4]     МОЩНОСТЬ РАССЕИВАЕМАЯ     приблизительная цена      Даташит
        # calculated coefficients - calc_coef     # device_dissipation      # approx_price            # datasheet

        with conn_l:
            conn_l.execute("""
                CREATE TABLE if not exists DIODES (
                    id_d INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    name_diode TEXT,
                    type_of_diode INTEGER,
                    current_max INTEGER,
                    voltage_max INTEGER,
                    body_version INTEGER,
                    checkpoints TEXT,
                    calc_coef REAL,
                    device_dissipation REAL,
                    approx_price REAL,
                    datasheet TEXT,
                    manufacturer INTEGER
                );
            """)

        # РЕЗИСТОРЫ
        # НОМИНАЛ РЕЗИСТОРА Om        ТОЧНОСТЬ РЕЗИСТОРА(РЯД)      МОЩНОСТЬ РАССЕИВАЕМАЯ     макс_напряжение          ИСПОЛНЕНИЕ SMD/PIN      КОЛЛЕКЦИЯ ВНУТР/ПОЛЬЗОВАТЕЛЬСКАЯ
        # resistance                  #e_row                       resistor_dissipation      resistor_max_v           body_version            collection_owner
        with conn_l:
            conn_l.execute("""
                CREATE TABLE if not exists RESISTORS (
                    id_r INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    resistance INTEGER,
                    e_row INTEGER,
                    resistor_dissipation REAL,
                    resistor_max_v REAL,
                    body_version TEXT,
                    collection_owner INTEGER
                );
            """)

         # КОНДЕНСАТОРЫ
         # НОМИНАЛ                  ТОЧНОСТЬ                       МАТЕРИАЛ                 ИСПОЛНЕНИЕ SMD/PIN       КОЛЛЕКЦИЯ





    def insert_resistors(self, list_resistors) -> None:
        print('insert resistors')
        sql_resistors = 'INSERT INTO RESISTORS (resistance, e_row, resistor_dissipation, resistor_max_v, body_version, collection_owner) values(?, ?, ?, ?, ?, ?)'
        # data = [
        #     (1, 'Alice', 21),
        #     (2, 'Bob', 22),
        #     (3, 'Chris', 23)
        # ]
        # for resistor in list_resistors:
        with conn_l:
            conn_l.executemany(sql_resistors, list_resistors)

    def get_e_resistors(e_row: int) -> list:
        with conn_l:
            list_resistors = conn_l.execute(
                "SELECT * FROM resistance WHERE e_row = {e_row}")
            # for row in data:
            # print(row)
        return list_resistors

    def generate_E_row_resistor(self, e_row: int) -> list:
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
                gen_E_row_resistors = round(
                    10**(n/list_E_row[e_row]), E_row_round[e_row])
        print(f'gen_E_row_resistors = {gen_E_row_resistors}')
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
        list_nominals = self.generate_E_row_resistor(e_row)

        gen_E_row_dim_resistor = []
        for resistir_nom in list_nominals:
            # sql_resistors = 'INSERT INTO RESISTORS (resistance, e_row, device_dissipation, resistor_max_v, body_version, collection_owner)'
            gen_E_row_dim_resistor.append([resistir_nom, e_row, max_power_resistor[r_dim],max_v_resistor[r_dim],dimension_resistor[r_dim],DEFAULT_LIST])

        return gen_E_row_dim_resistor

            

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

db = sqlite_database()
# в НАЧАЛЕ СОЗДАНИЕ БАЗ ДАННЫХ
# db.create_tables_base()


resistor_list_E24_R_0805 = db.generate_list_resistors(RES_E24,R_0805)
resistor_list_E96_R_0805 = db.generate_list_resistors(RES_E96,R_0805)
# print(f'resistor_list = {resistor_list_E96_R_0805}')
# db.insert_resistors(resistor_list_E24_R_0805)
# db.insert_resistors(resistor_list_E96_R_0805)

# Сериализация массивов
# list = [1, 2, [3, 4]]
# dump_string = json.dumps(list)  # '[1, 2, [3, 4]]'
# print('dump_string = ' + dump_string)
# list = json.loads(dump_string)
# print('list = ' + str(list))

# ОСНОВНЫЕ ПО ЧИПУ https://static.chipdip.ru/lib/057/DOC000057299.pdf
# Набор из 4 точек для построения кривой падения напряжения на диоде для 25 градусов
# SS16,   Шоттки, 50В, 1А,  SMD,  0,0.3,0.1,0.38,0.4,0.5,1.0,0.75,          SS16.pdf
# SS36,   Шоттки, 60В, 3А,  SMD,  0.01,0.31,0.2,0.43,1,0.52,3.0,0.70         SS32-SS320.pdf
# SS310,  Шоттки, 100В, 3А,  поверхностный,  0.01,0.47,0.2,0.56,1,0.65,3,0.85   SS32-SS320.pdf

# 1N5819,  Schottky, 40V, 1A,  PIN,  0.01,0.17,0.1,0.25,0.5,0.33,1,0.39,       1N5817-1N5819.pdf
# 1N5822 , Schottky,     40v, 3A,  PIN,  0.01,0.07,0.2,0.3,1,0.38,3,0.48,      1N5820-1N5822.pdf
# # БЫСТРОВОСТАНАВЛИВАЮЩИЕСЯ МОЩНЫЕ ДУМАЮ НА НИХ ХОРОШО СОБИРАТЬ МОСТ ВРУЧНУЮ С PFC 

# HER303,  PN, 3А, 200В ,  ШТЫРЬЕВОЙ,  0.01,0.51,0.3,0.52,1,0.8,3,0.9,    her301-308.pdf
# HER308,  PN, 3А, 1000В,  PIN,   0.01,0.4,0.3,1.1,1,1.25,3,1.5,         her301-308.pdf

 

#!!! Бывает общий даташит нужно формировать перечень файлов для импорта и сравнивать с теми что уже есть и добавлять только те что отсутствуюю
 


