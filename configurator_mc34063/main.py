import sys
from PyQt5 import QtWidgets, uic, QtWebEngineWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QBrush, QPainter, QPen, QPixmap, QPolygonF,QImage
from PyQt5.QtCore import Qt
from random import randint
 
# математика по микросхеме
from math_mc34063 import mc34063
# работа с sqlite
from database import database_lite
# окно загрузки компонентов
from service import service_load

math_mc = mc34063.math_mc34063()
db = database_lite.sqlite_database()
# table_components

# доп окна
# https://www.pythonguis.com/tutorials/creating-multiple-windows/

FILE_IMAGE_BUCK_SCHEME = r'configurator_mc34063/res/BUCK_SHEM_SIMPLE.PNG'

FILE_UI_MAIN_WINDOW = r"configurator_mc34063/res/mc34063_main.ui"

LABEL_MAIN_WINDOW = r'mc34063 расчет номиналов схем'
 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 
 
# ********************************************************************************

class MainWindow_mc():
# class MainWindow_mc(QtWidgets.QMainWindow):


    def __init__(self):
        # super().__init__()
        # self.w = None  

        self.component_load = service_load.load_component()# дополнительное окно


        self.ui = uic.loadUi(FILE_UI_MAIN_WINDOW)
        self.ui.setWindowTitle(LABEL_MAIN_WINDOW)

        self.add_image_dcdc_down(self.ui)

        math_mc.print_formuls(self.ui)
        
        #Контектное меню ! СТИЛИ НЕ НАСТРОЕНЫ!
        # self.ui.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.ui.customContextMenuRequested.connect(self.on_context_menu)
 
        self.ui.show()

        # self.button = QtWidgets.QPushButton("Push for Window")
        # self.button.clicked.connect(self.show_new_window)
        # self.setCentralWidget(self.button)
        # цепляем к кнопке событие нажатия клавиши
        self.ui.open_w_add_component.setCheckable(True)
        self.ui.open_w_add_component.triggered.connect(self.show_new_window)
        self.ui.open_w_add_component.triggered.connect(self.the_button_was_toggled)


    def show(self):
         self.ui.show()

    def hide(self):
        self.ui.hide()

    def close(self):
        self.ui.close()
 

    def isVisible(self)->bool:
        return self.ui.isVisible()
 

    def the_button_was_toggled(self, checked):
        print("Checked?", checked)


    def show_new_window(self, checked):        
    #     # if self.w is None:# если окно не создано создать инчаче используем
    #     #     self.w = AnotherWindow()
    #     # self.w.show()#наследуемый метод

    #     # else: странная ветка
    #     #     self.w.close()  # Close window.
    #     #     self.w = None  # Discard reference.
        print(f"self.component_load.isVisible()  = {self.component_load.isVisible()}")
 
        if self.component_load.isVisible():
            self.component_load.hide()
        else:
            self.component_load.show()
 
 
    # #Контектное меню
    # def on_context_menu(self, pos):
    #     context = QtWidgets.QMenu(self.ui)
    #     context.addAction(QtWidgets.QAction("Сохранить", self.ui))
    #     context.addAction(QtWidgets.QAction("Обьновить", self.ui))
    #     context.addAction(QtWidgets.QAction("Сбросить", self.ui))
    #     context.exec(self.ui.mapToGlobal(pos))


    def add_image_dcdc_down(self, ui)-> None:
        # print(ui.back_shema_img.scene())
        scene = QtWidgets.QGraphicsScene()
        ui.back_shema_img.setScene(scene)
        ui.back_shema_img.setAlignment(QtCore.Qt.AlignLeft)
        
        image_qt = QImage(FILE_IMAGE_BUCK_SCHEME)
        pic = QtWidgets.QGraphicsPixmapItem()

        # возможно так проще widget.setPixmap(QPixmap('otje.jpg')) но это для лейбла
        pic.setPixmap(QPixmap.fromImage(image_qt))
        # scene.setSceneRect(0, 0, 400, 400) 
        scene.addItem(pic)

 
# ********************************************************************************
 


#как то отдельно  но требует первоначальной инициализации перед интерфейсом
app = QtWidgets.QApplication(sys.argv)

main_w = MainWindow_mc()
# main_w.show() 

# app.exec() 
try:
    sys.exit(app.exec())
except:
    print("Exiting")












    