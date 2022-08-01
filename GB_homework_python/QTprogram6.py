import sys
from PyQt5 import QtWidgets, uic, QtWebEngineWidgets,QtCore
from PyQt5.QtGui import QBrush, QPainter, QPen, QPixmap, QPolygonF,QImage

app = QtWidgets.QApplication(sys.argv)
ui = uic.loadUi("GB_homework_python/mc34063_main.ui")
ui.setWindowTitle("mc34063 расчет номиналов схем")

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
ui.webWidget.setHtml(page)
 

print(ui.back_shema_img.scene())
scene = QtWidgets.QGraphicsScene()
ui.back_shema_img.setScene(scene)
ui.back_shema_img.setAlignment(QtCore.Qt.AlignCenter)

image_qt = QImage(r'GB_homework_python/BUCK_SHEM_SIMPLE.PNG')
pic = QtWidgets.QGraphicsPixmapItem()
pic.setPixmap(QPixmap.fromImage(image_qt))
# scene.setSceneRect(0, 0, 400, 400) 
scene.addItem(pic)

 
ui.show()
app.exec()
 

# sys.exit(app.exec_())