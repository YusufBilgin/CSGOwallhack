# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import pymem
import time
import re


class Ui_widget(object):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(350, 250)
        widget.setMinimumSize(QtCore.QSize(350, 250))
        widget.setMaximumSize(QtCore.QSize(350, 250))
        widget.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        widget.setMouseTracking(False)
        widget.setWindowTitle("CS:GO Wallhack")
        widget.setLocale(QtCore.QLocale(QtCore.QLocale.Turkish, QtCore.QLocale.Turkey))
        self.stop_button = QtWidgets.QPushButton(widget)
        self.stop_button.setGeometry(QtCore.QRect(170, 120, 131, 41))
        self.stop_button.setObjectName("stop_button")
        self.progressBar = QtWidgets.QProgressBar(widget)
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(20, 90, 281, 21))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(widget)
        self.label.setGeometry(QtCore.QRect(20, 10, 141, 21))
        self.label.setObjectName("label")
        self.run_button = QtWidgets.QPushButton(widget)
        self.run_button.setGeometry(QtCore.QRect(20, 120, 131, 41))
        self.run_button.setObjectName("run_button")
        self.label2 = QtWidgets.QLabel(widget)
        self.label2.setGeometry(QtCore.QRect(20, 50, 171, 21))
        self.label2.setText("")
        self.label2.setObjectName("label2")
        self.label_2 = QtWidgets.QLabel(widget)
        self.label_2.setGeometry(QtCore.QRect(10, 180, 331, 21))
        self.label_2.setLineWidth(1)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(widget)
        self.label_3.setGeometry(QtCore.QRect(40, 200, 291, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(widget)
        self.label_4.setGeometry(QtCore.QRect(40, 220, 281, 16))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(widget)
        QtCore.QMetaObject.connectSlotsByName(widget)

        self.run_button.clicked.connect(lambda: self.injectScript(2))
        self.stop_button.clicked.connect(lambda: self.injectScript(1))

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        self.stop_button.setText(_translate("widget", "Durdur"))
        self.label.setText(_translate("widget", "CS:GO wallhack hilesi"))
        self.run_button.setText(_translate("widget", "Çalıştır"))
        self.label_2.setText(_translate("widget", "Not: Hileyi durdurduktan sonra bağzı sistemlerde oyun "))
        self.label_3.setText(_translate("widget", "çökebilir. Oyunu yeniden başlattığınız zaman "))
        self.label_4.setText(_translate("widget", "herşey normal şekilde çalışacaktır."))

    def injectScript(self, x):
        try:
            pm = pymem.Pymem('csgo.exe')
            client = pymem.process.module_from_name(pm.process_handle,
                                                    'client.dll')
            clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
            address = client.lpBaseOfDll + re.search(rb'\x83\xF8.\x8B\x45\x08\x0F',
                                                     clientModule).start() + x
            pm.write_uchar(address, 2 if pm.read_uchar(address) == 1 else 1)
            pm.close_process()
            self.load_animation()
            if x == 2:
                self.label2.setText("Hile enjekte edildi")
            elif x == 1:
                self.label2.setText("Hile durduruldu")
        except:
            self.label2.setText("Görünen o ki csgo çalışmıyor")
        

    def load_animation(self):
        count = 0
        while count < 100:
            count += 5
            time.sleep(0.1)
            self.progressBar.setValue(count)
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_widget()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
