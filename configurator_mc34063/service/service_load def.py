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
 
# sys.exit(app.exec_())
# dialog_load.ui
# https://www-pythonguis-com.translate.goog/tutorials/pyqt-actions-toolbars-menus/?_x_tr_sl=en&_x_tr_tl=ru&_x_tr_hl=ru&_x_tr_pto=wapp
class load_component(QtWidgets.QWidget):
    """     This "window" is a QWidget. If it has no parent, it will appear as a free-floating window as we want.    """
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        self.label =  QtWidgets.QLabel("Another Window % d" % randint(0,100))
        layout.addWidget(self.label)
        self.setLayout(layout)

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
            QtWidgets.QCheckBox,			#   Флажок
            QtWidgets.QComboBox,            #  	Выпадающий список
            QtWidgets.QDateEdit,            #  	Для редактирования даты и даты и времени
            QtWidgets.QDateTimeEdit,        #  	Для редактирования даты и даты и времени
            QtWidgets.QDial,                #  	Поворотный циферблат
            QtWidgets.QDoubleSpinBox,       #  	Спиннер чисел для поплавков
            QtWidgets.QFontComboBox,        #  	Список шрифтов
            QtWidgets.QLCDNumber,           #  	Довольно уродливый ЖК-дисплей
            QtWidgets.QLabel,               #  	Просто ярлык, а не интерактив
            QtWidgets.QLineEdit,            #  	Введите строку текста
            QtWidgets.QProgressBar,         #  	Индикатор выполнения
            QtWidgets.QPushButton,          #  	Кнопка
            QtWidgets.QRadioButton,         #  	Набор переключателей только с одним активным элементом
            QtWidgets.QSlider,              #  	Ползунок
            QtWidgets.QSpinBox,             #  	Целочисленный счетчик
            QtWidgets.QTimeEdit            #  	Время редактирования
         ]

        for w in widgets:
            layout.addWidget(w())

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

if __name__ == '__main__':

    # mathematics = math_mc34063() 
    print('')
