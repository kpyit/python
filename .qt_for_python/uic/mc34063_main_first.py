# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\python\GB_homework_python\configurator_mc34063\mc34063_main_first.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(1260, 840)
        Dialog.setStyleSheet("QDialog { background-color: #272822;}\n"
"\n"
"QTabWidget { background-color: #272822;} /* не ясно на что влияет важен порядок вложенности*/\n"
"\n"
"QTabWidget::pane { /* The tab widget frame */\n"
"    border-top: 2px solid #676d73;\n"
"}\n"
"QTabWidget::tab-bar {\n"
"    left: 15px; /* move to the right by 5px */\n"
"}\n"
"/* Style the tab using the tab sub-control. Note that\n"
"    it reads QTabBar _not_ QTabWidget */\n"
"QTabBar::tab {\n"
"    color: White;\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #565657, stop: 1.0 #272822);\n"
"    border: 2px solid #676d73;\n"
"    border-bottom-color: #676d73; /* same as the pane color */\n"
"    border-top-left-radius: 2px;\n"
"    border-top-right-radius: 2px;\n"
"    min-width: 25ex;\n"
"    padding:2 10px;\n"
"}\n"
"\n"
"QTabBar::tab:selected, QTabBar::tab:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #91969c, stop:  1.0 #676d73);\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    border-color: #9B9B9B;\n"
"    border-bottom-color: #C2C7CB; /* same as pane color */\n"
"}\n"
"\n"
"QTabBar::tab:!selected {    margin-top: 2px; /* make non-selected tabs look smaller */}\n"
"/* make use of negative margins for overlapping tabs */\n"
"QTabBar::tab:selected {     /* expand/overlap to the left and right by 4px */    \n"
"    margin-left: -4px;\n"
"    margin-right: -4px;\n"
"}\n"
"QTabBar::tab:first:selected {    margin-left: 0; /* the first selected tab has nothing to overlap with on the left */}\n"
"QTabBar::tab:last:selected {    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */}\n"
"QTabBar::tab:only-one {    margin: 0; /* if there is only one tab, we don\'t want overlapping margins */}\n"
"\n"
"/* содержимое таба */\n"
"QWidget { background-color: #272822; }\n"
"\n"
"QPushButton { color: White; background-color: Green }\n"
"\n"
"QLineEdit { background-color: #f2f2f2; }\n"
"QTextEdit { background-color: #f2f2f2; }\n"
"QLabel {  color: White; }")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(20, 50, 1251, 831))
        self.tabWidget.setObjectName("tabWidget")
        self.Tab_1 = QtWidgets.QWidget()
        self.Tab_1.setObjectName("Tab_1")
        self.back_shema_img = QtWidgets.QGraphicsView(self.Tab_1)
        self.back_shema_img.setGeometry(QtCore.QRect(690, 0, 570, 445))
        self.back_shema_img.setObjectName("back_shema_img")
        self.calculate_back_simple = QtWidgets.QPushButton(self.Tab_1)
        self.calculate_back_simple.setGeometry(QtCore.QRect(10, 600, 93, 31))
        self.calculate_back_simple.setStyleSheet("")
        self.calculate_back_simple.setObjectName("calculate_back_simple")
        self.save_back_calc = QtWidgets.QPushButton(self.Tab_1)
        self.save_back_calc.setGeometry(QtCore.QRect(120, 600, 151, 31))
        self.save_back_calc.setObjectName("save_back_calc")
        self.lineEdit = QtWidgets.QLineEdit(self.Tab_1)
        self.lineEdit.setGeometry(QtCore.QRect(180, 20, 113, 22))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.textEdit = QtWidgets.QTextEdit(self.Tab_1)
        self.textEdit.setGeometry(QtCore.QRect(10, 480, 371, 111))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(self.Tab_1)
        self.label.setGeometry(QtCore.QRect(20, 20, 131, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.Tab_1)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 141, 21))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.Tab_1)
        self.lineEdit_2.setGeometry(QtCore.QRect(180, 60, 113, 22))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_3 = QtWidgets.QLabel(self.Tab_1)
        self.label_3.setGeometry(QtCore.QRect(10, 450, 151, 21))
        self.label_3.setObjectName("label_3")
        self.save_back_calc_2 = QtWidgets.QPushButton(self.Tab_1)
        self.save_back_calc_2.setGeometry(QtCore.QRect(290, 600, 91, 31))
        self.save_back_calc_2.setObjectName("save_back_calc_2")
        self.webWidget = QtWebEngineWidgets.QWebEngineView(self.Tab_1)
        self.webWidget.setGeometry(QtCore.QRect(440, 450, 811, 351))
        self.webWidget.setObjectName("webWidget")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.Tab_1)
        self.lineEdit_3.setGeometry(QtCore.QRect(180, 140, 113, 22))
        self.lineEdit_3.setText("")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_4 = QtWidgets.QLabel(self.Tab_1)
        self.label_4.setGeometry(QtCore.QRect(20, 100, 131, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.Tab_1)
        self.label_5.setGeometry(QtCore.QRect(20, 140, 141, 21))
        self.label_5.setObjectName("label_5")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.Tab_1)
        self.lineEdit_4.setGeometry(QtCore.QRect(180, 100, 113, 22))
        self.lineEdit_4.setText("")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_6 = QtWidgets.QLabel(self.Tab_1)
        self.label_6.setGeometry(QtCore.QRect(20, 180, 151, 21))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.Tab_1)
        self.label_7.setGeometry(QtCore.QRect(20, 220, 141, 21))
        self.label_7.setObjectName("label_7")
        self.open_w_add_component = QtWidgets.QPushButton(self.Tab_1)
        self.open_w_add_component.setGeometry(QtCore.QRect(390, 140, 171, 31))
        self.open_w_add_component.setObjectName("open_w_add_component")
        self.tabWidget.addTab(self.Tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.calculate_back_simple.setText(_translate("Dialog", "Расчет"))
        self.save_back_calc.setText(_translate("Dialog", "сохранить результат"))
        self.textEdit.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label.setText(_translate("Dialog", "Входное напряжение"))
        self.label_2.setText(_translate("Dialog", "Выходное напряжение"))
        self.label_3.setText(_translate("Dialog", "Комментарий к расчету"))
        self.save_back_calc_2.setText(_translate("Dialog", "загрузить"))
        self.label_4.setText(_translate("Dialog", "Выходная емкость"))
        self.label_5.setText(_translate("Dialog", "Выходной ток"))
        self.label_6.setText(_translate("Dialog", "Авторасчет частоты"))
        self.label_7.setText(_translate("Dialog", "Расчетная частота"))
        self.open_w_add_component.setText(_translate("Dialog", "Загрузить компоненты"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab_1), _translate("Dialog", "Понижающий(Buck)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Повышающий(Bust)"))
from PyQt5 import QtWebEngineWidgets
