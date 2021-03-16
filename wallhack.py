from PyQt5 import QtCore, QtGui, QtWidgets
import pymem.process
import keyboard
import pymem
import time
import sys
import re

dwEntityList = (0x4DA2F24)
dwLocalPlayer = (0xD8B2DC)
m_iTeamNum = (0xF4)
dwGlowObjectManager = (0x52EB518)
m_iGlowIndex = (0xA438)


class Ui_widget(object):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(637, 339)
        widget.setMinimumSize(QtCore.QSize(637, 339))
        widget.setMaximumSize(QtCore.QSize(637, 339))
        self.groupBox = QtWidgets.QGroupBox(widget)
        self.groupBox.setGeometry(QtCore.QRect(20, 240, 241, 91))
        self.groupBox.setObjectName("groupBox")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(10, 40, 93, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(120, 40, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.groupBox_2 = QtWidgets.QGroupBox(widget)
        self.groupBox_2.setGeometry(QtCore.QRect(280, 240, 241, 91))
        self.groupBox_2.setObjectName("groupBox_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 40, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_4.setGeometry(QtCore.QRect(120, 40, 93, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.groupBox_3 = QtWidgets.QGroupBox(widget)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 150, 201, 80))
        self.groupBox_3.setObjectName("groupBox_3")
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_5.setGeometry(QtCore.QRect(10, 30, 171, 28))
        self.pushButton_5.setObjectName("pushButton_5")
        self.imageLabel = QtWidgets.QLabel(widget)
        self.imageLabel.setGeometry(QtCore.QRect(240, 10, 390, 219))
        self.pixmap = QtGui.QPixmap("img/ekremabi.png")
        self.imageLabel.setPixmap(self.pixmap)
        self.progressBar = QtWidgets.QProgressBar(widget)
        self.progressBar.setGeometry(QtCore.QRect(20, 100, 201, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(widget)
        self.label.setGeometry(QtCore.QRect(540, 310, 91, 21))
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(widget)
        self.line.setGeometry(QtCore.QRect(20, 130, 201, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(widget)
        self.line_2.setGeometry(QtCore.QRect(20, 70, 201, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_2 = QtWidgets.QLabel(widget)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 161, 21))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(widget)
        QtCore.QMetaObject.connectSlotsByName(widget)

        self.pushButton.clicked.connect(lambda: self.injectScript("enemy", True))
        self.pushButton_2.clicked.connect(lambda: self.injectScript("enemy", False))
        self.pushButton_3.clicked.connect(lambda: self.injectScript("counter", True))
        self.pushButton_4.clicked.connect(lambda: self.injectScript("counter", False))
        self.pushButton_5.clicked.connect(lambda: self.injectScript("all", True))


    def injectScript(self, team, value):
        if team == "enemy":
            pass
        elif team == "counter":
            pass
        elif team == "all":
            pass
        else:
            pass


    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "CS:GO Wallhack"))
        self.groupBox.setTitle(_translate("widget", "Bizim Takım"))
        self.pushButton.setText(_translate("widget", "fosforlu"))
        self.pushButton_2.setText(_translate("widget", "Normal"))
        self.groupBox_2.setTitle(_translate("widget", "Düşman Takım"))
        self.pushButton_3.setText(_translate("widget", "fosforlu"))
        self.pushButton_4.setText(_translate("widget", "Normal"))
        self.groupBox_3.setTitle(_translate("widget", "Herkez"))
        self.pushButton_5.setText(_translate("widget", "Herkezi saydam mavi yap"))
        self.label.setText(_translate("widget", "© 2021 | v0.2"))
        self.label_2.setText(_translate("widget", "Hile enjekte edildi"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_widget()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
