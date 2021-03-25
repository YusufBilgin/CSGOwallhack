from PyQt5.QtCore import (
    QObject,
    QThread,
    pyqtSignal,
    QRect,
    QSize,
    Qt
)
from PyQt5.QtWidgets import (
    QProgressBar,
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QGroupBox,
    QFrame
)
from PyQt5.QtGui import QPixmap
import pymem.process
import keyboard
import pymem
import sys
import re

# csgo offsets
dwEntityList = (0x4DA3F44)
dwLocalPlayer = (0xD8C2CC)
m_iTeamNum = (0xF4)
dwGlowObjectManager = (0x52EC558)
m_iGlowIndex = (0xA438)


# worker class
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, parent = None):
        QObject.__init__(self, parent = parent)
        self.continue_run = True

    def run(self):
        pm = pymem.Pymem("csgo.exe")
        client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

        while self.continue_run:
            glow_manager = pm.read_int(client + dwGlowObjectManager)

            for i in range(1, 32):
                entity = pm.read_int(client + dwEntityList + i * 0x10)

                if entity:
                    entity_team_id = pm.read_int(entity + m_iTeamNum)
                    entity_glow = pm.read_int(entity + m_iGlowIndex)
                    if entity_team_id == 2:
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(1))
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)
        self.finished.emit()


class Window(QMainWindow):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi()  # Creates all required graphical components

    def setupUi(self):

        # Window
        self.setWindowTitle("CS:GO Wallhack")
        self.resize(637, 339)
        self.setMinimumSize(QSize(637, 339))
        self.setMaximumSize(QSize(637, 339))

        # create widgets
        self.groupBox = QGroupBox("Bizim Takım", self)
        self.groupBox.setGeometry(QRect(20, 240, 241, 91))
        self.groupBox.setObjectName("groupBox")
        self.counterEnableButton = QPushButton("fosforlu", self.groupBox)
        self.counterEnableButton.setGeometry(QRect(10, 40, 93, 31))
        self.counterEnableButton.setObjectName("pushButton")
        self.counterDisableButton = QPushButton("Normal", self.groupBox)
        self.counterDisableButton.setGeometry(QRect(120, 40, 93, 28))
        self.counterDisableButton.setObjectName("pushButton_2")
        self.groupBox_2 = QGroupBox("Düşman Takım", self)
        self.groupBox_2.setGeometry(QRect(280, 240, 241, 91))
        self.groupBox_2.setObjectName("groupBox_2")
        self.terroristEnableButton = QPushButton("fosforlu", self.groupBox_2)
        self.terroristEnableButton.setGeometry(QRect(10, 40, 93, 28))
        self.terroristEnableButton.setObjectName("pushButton_3")
        self.terroristDisableButton = QPushButton("Normal", self.groupBox_2)
        self.terroristDisableButton.setGeometry(QRect(120, 40, 93, 28))
        self.terroristDisableButton.setObjectName("pushButton_4")
        self.groupBox_3 = QGroupBox("Herkez", self)
        self.groupBox_3.setGeometry(QRect(20, 150, 201, 80))
        self.groupBox_3.setObjectName("groupBox_3")
        self.pushButton_5 = QPushButton("Herkezi saydam mavi yap", self.groupBox_3)
        self.pushButton_5.setGeometry(QRect(10, 30, 171, 28))
        self.pushButton_5.setObjectName("pushButton_5")
        self.imageLabel = QLabel("© 2021 | v0.2", self)
        self.imageLabel.setGeometry(QRect(240, 10, 390, 219))
        self.pixmap = QPixmap("img/ekremabi.png")
        self.imageLabel.setPixmap(self.pixmap)
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(QRect(20, 100, 201, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label = QLabel(self)
        self.label.setGeometry(QRect(540, 310, 91, 21))
        self.label.setObjectName("label")
        self.line = QFrame(self)
        self.line.setGeometry(QRect(20, 130, 201, 16))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QFrame(self)
        self.line_2.setGeometry(QRect(20, 70, 201, 16))
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QRect(20, 30, 161, 21))
        self.label_2.setObjectName("label_2")

        # Connections
        self.counterEnableButton.clicked.connect(lambda: self.run_script())
        self.terroristEnableButton.clicked.connect(lambda: self.run_script())

    def run_script(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
        self.counterDisableButton.clicked.connect(self.stop_thread)


        self.counterEnableButton.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.counterDisableButton.setEnabled(True)
        )

    def stop_thread(self):
        print("trying to stop")
        self.worker.continue_run = False


app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec_())
