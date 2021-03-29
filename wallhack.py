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
import time
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
    progress = pyqtSignal()

    def __init__(self, parent = None):
        QObject.__init__(self, parent = parent)
        self.ct_continue_run = True
        self.t_continue_run = True

    def glow_counter(self):
        pm = pymem.Pymem("csgo.exe")
        client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

        while self.ct_continue_run:
            glow_manager = pm.read_int(client + dwGlowObjectManager)

            for i in range(1, 32):
                entity = pm.read_int(client + dwEntityList + i * 0x10)

                if entity:
                    entity_team_id = pm.read_int(entity + m_iTeamNum)
                    entity_glow = pm.read_int(entity + m_iGlowIndex)
                    if entity_team_id == 3:
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0))
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)
        self.finished.emit()

    def glow_terrorist(self):
        pm = pymem.Pymem("csgo.exe")
        client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

        while self.t_continue_run:
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
        self.groupBox_ct = QGroupBox("Counter Strike", self)
        self.groupBox_ct.setGeometry(QRect(20, 240, 241, 91))
        self.groupBox_ct.setObjectName("groupBox_ct")
        self.counterEnableButton = QPushButton("fosforlu", self.groupBox_ct)
        self.counterEnableButton.setGeometry(QRect(10, 40, 93, 31))
        self.counterEnableButton.setObjectName("counterEnableButton")
        self.counterDisableButton = QPushButton("Normal", self.groupBox_ct)
        self.counterDisableButton.setGeometry(QRect(120, 40, 93, 28))
        self.counterDisableButton.setObjectName("counterDisableButton")
        self.groupBox_t = QGroupBox("Terörist", self)
        self.groupBox_t.setGeometry(QRect(280, 240, 241, 91))
        self.groupBox_t.setObjectName("groupBox_t")
        self.terroristEnableButton = QPushButton("fosforlu", self.groupBox_t)
        self.terroristEnableButton.setGeometry(QRect(10, 40, 93, 28))
        self.terroristEnableButton.setObjectName("terroristEnableButton")
        self.terroristDisableButton = QPushButton("Normal", self.groupBox_t)
        self.terroristDisableButton.setGeometry(QRect(120, 40, 93, 28))
        self.terroristDisableButton.setObjectName("terroristDisableButton")
        self.groupBox_all = QGroupBox("Herkez", self)
        self.groupBox_all.setGeometry(QRect(20, 150, 201, 80))
        self.groupBox_all.setObjectName("groupBox_all")
        self.makeAllBlueButton = QPushButton("Herkezi saydam mavi yap", self.groupBox_all)
        self.makeAllBlueButton.setGeometry(QRect(10, 30, 171, 28))
        self.makeAllBlueButton.setObjectName("pushButton_5")
        self.imageLabel = QLabel("© 2021 | v0.2", self)
        self.imageLabel.setGeometry(QRect(240, 10, 390, 219))
        self.pixmap = QPixmap("img/ekremabi.png")
        self.imageLabel.setPixmap(self.pixmap)
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(QRect(20, 100, 201, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label = QLabel("© 2021 | v0.2", self)
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
        self.counterEnableButton.clicked.connect(lambda: self.run_script("counter"))
        self.terroristEnableButton.clicked.connect(lambda: self.run_script("terrorist"))
        self.counterDisableButton.clicked.connect(lambda: self.stop_thread("counter"))
        self.terroristDisableButton.clicked.connect(lambda: self.stop_thread("terrorist"))
        self.makeAllBlueButton.clicked.connect(self.make_all_blue)


    def run_script(self, team):
        if team == "counter":
            # create worker object
            self.ct_thread = QThread()
            self.ct_worker = Worker()
            self.ct_worker.moveToThread(self.ct_thread)

            # Signals
            self.ct_thread.started.connect(self.ct_worker.glow_counter)
            self.ct_worker.finished.connect(self.ct_thread.quit)
            self.ct_worker.finished.connect(self.ct_worker.deleteLater)
            self.ct_thread.finished.connect(self.ct_thread.deleteLater)

            self.ct_thread.start()
            self.load_animation()

            self.counterEnableButton.setEnabled(False)
            self.ct_thread.finished.connect(
                lambda: self.counterEnableButton.setEnabled(True)
            )
        elif team == "terrorist":
            # create worker object
            self.t_thread = QThread()
            self.t_worker = Worker()
            self.t_worker.moveToThread(self.t_thread)

            # Signals
            self.t_thread.started.connect(self.t_worker.glow_terrorist)
            self.t_worker.finished.connect(self.t_thread.quit)
            self.t_worker.finished.connect(self.t_worker.deleteLater)
            self.t_thread.finished.connect(self.t_thread.deleteLater)

            self.t_thread.start()
            self.load_animation()

            self.terroristEnableButton.setEnabled(False)
            self.t_thread.finished.connect(
                lambda: self.terroristEnableButton.setEnabled(True)
            )

    def stop_thread(self, team):
        # print("trying to stop")
        if team == "counter":
            self.ct_worker.ct_continue_run = False
        elif team == "terrorist":
            self.t_worker.t_continue_run = False

    def make_all_blue(self):
        try:
            processName='csgo.exe'
            pm = pymem.Pymem(processName)
            client = pymem.process.module_from_name(pm.process_handle,'client.dll')

            clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
            address = client.lpBaseOfDll + re.search(rb'\x83\xF8.\x8B\x45\x08\x0F',
                                                  clientModule).start() + 2

            pm.write_uchar(address, 2 if pm.read_uchar(address) == 1 else 1)
            pm.close_process()
            self.load_animation()

            print("hack completed")

        except:
            print("error: couldn't find process",processName)

    def load_animation(self):
        count = 0
        while count < 100:
            count += 10
            time.sleep(0.1)
            self.progressBar.setValue(count)


app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec_())
