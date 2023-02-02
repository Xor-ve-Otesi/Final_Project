import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from ui import Ui_MainWindow
import socket
from time import sleep

addr = socket.getaddrinfo("192.168.61.141", 1235)[0][-1]
ServerSideSocket = socket.socket()
ServerSideSocket.bind(addr)
ServerSideSocket.listen(5)
conn, address = ServerSideSocket.accept()  # accept new connection

class Worker(QObject):
    progress = pyqtSignal(int)

    def run(self):


        while True:
            #data = conn.recv(1024).decode()
            sleep(0.2)
            self.progress.emit(0)


class Lab4():
    def __init__(self) -> None:

        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.button_initiator()
        self.motor_speed_1 = 0
        self.motor_speed_2 = 0
        self.motor_speed_1_s = 0
        self.motor_speed_2_s = 0
        self.motor_speed_1_m = 0
        self.motor_speed_2_m = 0
        self.motor_speed_1_h = 0
        self.motor_speed_2_h = 0
        self.ui.Motor1.setMaximum(100)
        self.ui.Motor2.setMaximum(100)
        self.runLongTask()

    def button_initiator(self):
        self.ui.Motor1.sliderReleased.connect(self.motor_1_changed)
        self.ui.Motor2.sliderReleased.connect(self.motor_2_changed)
        self.ui.S_button.clicked.connect(self.speed_s)
        self.ui.M_button.clicked.connect(self.speed_m)
        self.ui.H_button.clicked.connect(self.speed_h)
        self.ui.StopButton.clicked.connect(self.stopping)
        self.ui.S_cal.clicked.connect(self.calibrate_s)
        self.ui.M_cal.clicked.connect(self.calibrate_m)
        self.ui.H_cal.clicked.connect(self.calibrate_h)

    def calibrate_s(self):
        self.motor_speed_1_s = self.ui.Motor1.value()
        self.motor_speed_2_s = self.ui.Motor2.value()

    def calibrate_m(self):
        self.motor_speed_1_m = self.ui.Motor1.value()
        self.motor_speed_2_m = self.ui.Motor2.value()

    def calibrate_h(self):
        self.motor_speed_1_h = self.ui.Motor1.value()
        self.motor_speed_2_h = self.ui.Motor2.value()

    def speed_s(self):
        self.ui.Motor1.setValue(self.motor_speed_1_s)
        self.ui.Motor2.setValue(self.motor_speed_2_s)
        self.motor_speed_1 = self.motor_speed_1_s
        self.motor_speed_2 = self.motor_speed_2_s

    def speed_m(self):
        self.ui.Motor1.setValue(self.motor_speed_1_m)
        self.ui.Motor2.setValue(self.motor_speed_2_m)
        self.motor_speed_1 = self.motor_speed_1_m
        self.motor_speed_2 = self.motor_speed_2_m

    def speed_h(self):
        self.ui.Motor1.setValue(self.motor_speed_1_h)
        self.ui.Motor2.setValue(self.motor_speed_2_h)
        self.motor_speed_1 = self.motor_speed_1_h
        self.motor_speed_2 = self.motor_speed_2_h

    def motor_1_changed(self):
        self.motor_speed_1 = self.ui.Motor1.value()

    def motor_2_changed(self):
        self.motor_speed_2 = self.ui.Motor2.value()

    def stopping(self):
        self.ui.Motor1.setValue(0)
        self.ui.Motor2.setValue(0)
        self.motor_speed_1 = 0
        self.motor_speed_2 = 0

    def runLongTask(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.reportProgress)
        self.thread.start()

    def reportProgress(self,num):
        conn.sendall(f"0,{self.motor_speed_1},{self.motor_speed_2},0".encode())
        print(f"0,{self.motor_speed_1},{self.motor_speed_2},0")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    lab4 = Lab4()
    lab4.MainWindow.show()
    sys.exit(app.exec_())