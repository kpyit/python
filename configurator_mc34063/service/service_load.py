from database import database_lite
from math_mc34063 import mc34063
import os.path
from os.path import exists
import sys
import warnings
import shutil

import re
import json
from enum import Enum, IntEnum
import numpy as np
import json
import matplotlib.pyplot as plt


if sys.version_info[0] < 3:  # (3, 0, 0, 'beta', 2)
    warnings.warn("Для выполнения этой программы необходима как минимум \
        версия Python 3.0",
                  RuntimeWarning)

__version__ = '0.1'

# основные виджет для окна
import PyQt5
from PyQt5 import QtWidgets, uic, QtWebEngineWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QTableWidget
from PyQt5.QtGui import QBrush, QPainter, QPen, QPixmap, QPolygonF, QImage
from PyQt5.QtCore import Qt


# динамическое построение графика в окне
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


# КОНСТАНТЫ ТИПОВ ДИОДА
# type_of_diode
D_TYPE_NONE = 0
D_TYPE_PN = 1
D_TYPE_SCHOTTKY = 2
D_TYPE_FIELD_TRANS = 3
TYPE_DIODE = (' ', 'полупровод.', 'шотки', 'транзистор')


# ИЗВЕСТНЫЕ ФИРМЫ ПРОИЗВОДИТЕЛИ
# manufacturer
ON_SEMICONDUCTOR = 1
TEXAS_INSTRUMENTS = 2
VISHAY = 3

# исполнение
TYPE_SMD = 1
TYPE_PIN = 2

# Временно пути к вложенным каталогам
PATH_IMPORT = r'configurator_mc34063/diodes_import/'
PATH_DATASHEETS = r'configurator_mc34063/datasheets/'
FILE_IMPORT_DIODES_TEXT = r'import_diodes.txt'
FILE_IMPORT_DIODES_SVF = r'import_diodes.csv'

LABEL_LOAD_COMPONENT = r'ЗАГРУЗКА КОМПОНЕНТОВ'
FILE_UI_LOAD_COMPONENT = r'configurator_mc34063/res/dialog_load.ui'


POSITION_DATASHEET = 7


# работа с sqlite
# можно попробовать в родителе создавать подключение в __init__ и проверять если не кустой обьект то создать подключение

db = database_lite.sqlite_database()

# математика по микросхеме
math_mc = mc34063.math_mc34063()


# [['SS16', 2, 50, 1000.0, 1, '[[0.01, 0.2, 0.5, 1.0], [0.3, 0.43, 0.54, 0.65]]', '[]', 'SS16.pdf'],

class imp_l(IntEnum):
    POS_NAME = 0
    POS_TYPE = 1
    POS_V = 2
    POS_A = 3
    POS_TYPE_B = 4
    POS_POINTS = 5
    POS_FACTORS = 6
    POS_DATASHEET = 7


BODY_SMD = 1
DODY_PIN = 2
BODY_TYPE = (' ', 'поверхнст.', 'штыревой')


# sys.exit(app.exec_())
# dialog_load.ui
# https://www-pythonguis-com.translate.goog/tutorials/pyqt-actions-toolbars-menus/?_x_tr_sl=en&_x_tr_tl=ru&_x_tr_hl=ru&_x_tr_pto=wapp
class load_component():
    """ диалоговое окно загруки списка компонентов """

    def __init__(self):

        self.ui_load = uic.loadUi(FILE_UI_LOAD_COMPONENT)
        self.ui_load.setWindowTitle(LABEL_LOAD_COMPONENT)

        self.ui_load.show()

        self.table = self.ui_load.table_components
        # self.table = QTableWidget()
        self.table.setColumnWidth(0, 120)
        self.table.setColumnWidth(1, 130)
        self.table.setColumnWidth(2, 130)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 130)
        self.table.setColumnWidth(5, 330)
        self.table.setColumnWidth(6, 200)

        # db.get_e_resistors()

        self.list_diodes = []
        self.file_to_load = ''

        # Виджет для отрисовки ===================

        # отрисовка виджета https://matplotlib.org/3.2.1/gallery/user_interfaces/embedding_in_qt_sgskip.html
        layout = QtWidgets.QVBoxLayout(self.ui_load.widget_draw)

        # автограницы в qt5 работают только так  - tight_layout=True  https://github.com/matplotlib/matplotlib/issues/10361/
        self.static_canvas = FigureCanvas(
            Figure(figsize=(3, 3), tight_layout=True))
        # layout.addWidget(NavigationToolbar(self.static_canvas,self.ui_load.widget_draw))# клавиши
        layout.addWidget(self.static_canvas)
        self._static_ax = self.static_canvas.figure.subplots()

        # ===================

        #  пока автоподгрузка заменить на загрузку из выбранного файла по кнопке
        self.list_diodes = self.import_diodes_info()
        self.table_insert_diodes(self.list_diodes)

        # бесполезно на этапе инициализации вызывать перерисовку она не работает
        # self.draw_avch_current_diode(self.list_diodes[0])
        self.draw_avch_current_diode(self.list_diodes[0])

        # math_mc.test_plot_diode_forvard_v(list_diodes[0])

        # ******************************************************
        # перерисовка графика по выбору ячейки пользователем
        self.table.selectionModel().selectionChanged.connect(self.on_selectionChanged)

        # ******************************************************
        # select_load_file
        # reload_file
 
        self.ui_load.select_load_file.clicked.connect(self.select_file)

        self.ui_load.reload_file.clicked.connect(self.reload_file)
 
        # def __init__(self):


    def select_file(self):
        file_filter = 'Data File (*.txt *.csv *.dat);; C File (*.h)'
        response = QtWidgets.QFileDialog.getOpenFileName(
            parent=None,
            caption='Выдерите файл для загрузки',
            # directory=os.getcwd(),
            directory='./configurator_mc34063/diodes_import',
            filter=file_filter,
            initialFilter='Data File (*.txt *.csv *.dat)'
        )
        
        print(f"response {response}")

        print(f"len(response[0]) != 0 {len(response[0]) != 0}")
        if(len(response[0]) != 0):
            self.file_to_load = response[0]
            print(f"self.file_to_load {self.file_to_load}")
            self.list_diodes = self.import_diodes_info()
            self.table_insert_diodes(self.list_diodes)


        # return response[0]

    # def select_file():
    #     '''Выбор файла загруки контента пользователем'''
    #     dlg = QtWidgets.QFileDialog()
    #     dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
    #     dlg.setFilter("Text files (*.txt)")
    #     # filenames = PyQt5.QStringList()

    #     if dlg.exec_():
    #         filenames = [dlg.selectedFiles()]
    #     print(filenames)

    def reload_file(self):
        '''Перезагрузка файла выбранного пользователем для обновления таблицы'''
        self.import_diodes_info()
        self.table_insert_diodes(self.list_diodes)

    def draw_avch_current_diode(self, diode):

        max_current = diode[imp_l.POS_A]/1000

        points_x_y = json.loads(diode[imp_l.POS_POINTS])
        print(f'points_x_y {points_x_y}')
        points_x = points_x_y[0]
        points_y = points_x_y[1]
        xnew = np.linspace(np.min(points_x), max_current, 100)

        coef = json.loads(diode[imp_l.POS_FACTORS])
        cubic_regression = np.poly1d(coef)
        ynew = cubic_regression(xnew)

        # отрисовка

        # self._static_ax.figure.clear(True) #жейтствительно чистит но не дает отрисовывать
        self._static_ax.clear()

        # https://matplotlib.org/stable/tutorials/introductory/usage.html#sphx-glr-tutorials-introductory-usage-py
        # self._static_ax.set_yscale('log')
        # self._static_ax.set_xscale('log')
        self._static_ax.plot(points_y, points_x, 'o',
                             label="заданные точки", color='red')
        self._static_ax.plot(
            ynew, xnew, label="расчетная кривая", color='green')
        self._static_ax.set_title(
            f'Расчетная характеристика диода {diode[imp_l.POS_NAME]} по точкам')
        self._static_ax.legend(loc='upper left')
        self._static_ax.set_xlabel('падение напряжения')
        self._static_ax.set_ylabel('ток через диод')
        # self._static_ax.set_ylim(np.min(points_x), max_current)
        # https://stackoverflow.com/questions/60020071/why-is-the-grid-turned-on-only-on-the-last-subplot
        self._static_ax.grid(b=True, which='major',
                             color='#777777', linestyle='-', alpha=0.2)

        # решило проблему наслоения осей но работает только со 2 раза в qt5 лечится  tight_layout=True
        # self.static_canvas.figure.tight_layout()

        self._static_ax.figure.canvas.draw()
        # вариант решения перерисовки
        # self.static_canvas.updateGeometry()

        # self.static_canvas.clf()
        # как еще вариант
        # scene = QtWidgets.QGraphicsScene()
        # figure = Figure()
        # axes = figure.gca()
        # axes.set_title("title")
        # axes.plot(plt.contourf(xx, yy, Z,cmap=plt.cm.autumn, alpha=0.8))
        # canvas = FigureCanvas(figure)
        # canvas.setGeometry(0, 0, 500, 500)
        # scene.addWidget(canvas)
        # self.setScene(scene)


    def on_selectionChanged(self, selected, deselected):
        for ix in selected.indexes():
            print('Selected Cell Location Row: {0}, Column: {1}'.format(
                ix.row(), ix.column()))
            # по селекту вызывать отрисовку стоки если список элементов не пуст

            self.draw_avch_current_diode(self.list_diodes[ix.row()])

        for ix in deselected.indexes():
            print('Deselected Cell Location Row: {0}, Column: {1}'.format(
                ix.row(), ix.column()))

    def show(self):
        self.ui_load.show()

    def hile(self):
        self.ui_load.hide()

    def isVisible(self) -> bool:
        return self.ui_load.isVisible()

    def load_diodes_from_file(self):
        print('')

    def table_insert_diodes(self, list_diodes: list):
        ''' Заполнение таблицы списком доступных диодов '''

        self.table.clear()
        self.table.setRowCount(len(list_diodes))
        # ['SS16', 2, 50, 1000.0, 1, '[[0.01, 0.2, 0.5, 1.0], [0.3, 0.43, 0.54, 0.65]]', '[]', 'SS16.pdf']
        row = 0
        for diode in list_diodes:
            self.table.setItem(
                row, 0, QtWidgets.QTableWidgetItem(diode[imp_l.POS_NAME]))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(
                TYPE_DIODE[diode[imp_l.POS_TYPE]]))
            self.table.setItem(
                row, 2, QtWidgets.QTableWidgetItem(str(diode[imp_l.POS_V])))
            self.table.setItem(
                row, 3, QtWidgets.QTableWidgetItem(str(diode[imp_l.POS_A])))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(
                BODY_TYPE[diode[imp_l.POS_TYPE_B]]))
            self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(
                str(diode[imp_l.POS_POINTS])))
            self.table.setItem(row, 6, QtWidgets.QTableWidgetItem(
                str(diode[imp_l.POS_DATASHEET])))
            row = row+1

    def copy_new_datasheets(self, list_diodes) -> None:
        list_datasheets = [x[POSITION_DATASHEET] for x in list_diodes]
        print(f'list_datasheets {list_datasheets}')

        for data in list_datasheets:
            print(
                f'{exists(PATH_IMPORT+data)} and {not exists(PATH_DATASHEETS+data)}')
            # print(f'{exists(PATH_IMPORT+data) and (not exists(PATH_DATASHEETS+data))}')
            if exists(PATH_IMPORT+data) and (not exists(PATH_DATASHEETS+data)):
                shutil.copyfile(PATH_IMPORT+data, PATH_DATASHEETS+data)

    def import_diodes_info(self) -> list:
        ''' импортирует перечень диодов с даташитами и расчитывает коэф ур Лагранжа
        '''
        name_type_diodes_shottky = {'шотки', 'шоттки', 'schottky'}
        name_type_diodes_semiconductor = {'pn', 'np', 'полупроводниковый', ''}
        type_mount_sm = {'поверхностный', 'smd'}
        type_mount_pin = {'штыревой', 'pin'}
        list_diodes = []
 
        file_path = r''

        print(f"len(self.file_to_load) != 0) {len(self.file_to_load) != 0} ")
        print(f"os.path.exists(self.file_to_load) {os.path.exists(self.file_to_load)}")
        if(len(self.file_to_load) != 0) and os.path.exists(self.file_to_load):
            file_path = self.file_to_load
        elif(os.path.exists(PATH_IMPORT+FILE_IMPORT_DIODES_TEXT)):
            file_path = PATH_IMPORT+FILE_IMPORT_DIODES_TEXT


        if(len(file_path) !=0):
            with open(file_path, mode="r", encoding="utf-8") as f:
                for line in f.readlines():
                    if not line.startswith("#"):
                        diode = []
                        line = re.sub(r'(^[ \t\n]+|[ \t\n]+)',
                                      '', line, flags=re.M)
                        diode_params = re.split(",", line, flags=re.UNICODE)
                        print(
                            f'line {diode_params} len(line)={len(diode_params)} ')
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

                        # генерация коэф по точкам
                        # Помойму это не по канонам Питона!
                        x_list = [float(x) for id, x in enumerate(
                            diode_params[5:13]) if id % 2 == 0]
                        y_list = [float(y) for id, y in enumerate(
                            diode_params[5:13]) if id % 2 == 1]
                        diode.append(json.dumps([x_list, y_list]))

                        #
                        coef = math_mc.calc_coef_regression(
                            diode[imp_l.POS_POINTS])
                        diode.append(json.dumps(coef))

                        # print(f'datasheet {diode_params[13]}')
                        diode.append(diode_params[13])
                        list_diodes.append(diode)

        # print(f'list_diodes {list_diodes}')
        
        return list_diodes


# !есть предопределенные темные стили для окон!
    # num_rows, num_cols = 10, 10

    # app = QtGui.QApplication(sys.argv)
    # w = QtGui.QTableWidget()
    # w.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    # w.setRowCount(num_rows)
    # w.setColumnCount(num_cols)
    # w.setAlternatingRowColors(True)

    # for i in xrange(num_rows):
    #     for j in xrange(num_cols):
    #         w.setItem(i, j, QtGui.QTableWidgetItem('test'))

    # добавление кучи виджетов для поиграться


    def test_widgets(self):

        layout = QVBoxLayout()
        widgets = [
            QtWidgets.QCheckBox,  # Флажок
            QtWidgets.QComboBox,  # Выпадающий список
            QtWidgets.QDateEdit,  # Для редактирования даты и даты и времени
            QtWidgets.QDateTimeEdit,  # Для редактирования даты и даты и времени
            QtWidgets.QDial,  # Поворотный циферблат
            QtWidgets.QDoubleSpinBox,  # Спиннер чисел для поплавков
            QtWidgets.QFontComboBox,  # Список шрифтов
            QtWidgets.QLCDNumber,  # Довольно уродливый ЖК-дисплей
            QtWidgets.QLabel,  # Просто ярлык, а не интерактив
            QtWidgets.QLineEdit,  # Введите строку текста
            QtWidgets.QProgressBar,  # Индикатор выполнения
            QtWidgets.QPushButton,  # Кнопка
            QtWidgets.QRadioButton,  # Набор переключателей только с одним активным элементом
            QtWidgets.QSlider,  # Ползунок
            QtWidgets.QSpinBox,  # Целочисленный счетчик
            QtWidgets.QTimeEdit  # Время редактирования
        ]

        for w in widgets:
            layout.addWidget(w())

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.ui.setCentralWidget(widget)


if __name__ == '__main__':

    # mathematics = math_mc34063()
    print('')

    form_load = load_component()
