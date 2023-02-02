# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'v1.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(760, 464)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Motor1 = QtWidgets.QSlider(self.centralwidget)
        self.Motor1.setGeometry(QtCore.QRect(60, 70, 671, 31))
        self.Motor1.setOrientation(QtCore.Qt.Horizontal)
        self.Motor1.setObjectName("Motor1")
        self.Motor2 = QtWidgets.QSlider(self.centralwidget)
        self.Motor2.setGeometry(QtCore.QRect(60, 140, 671, 31))
        self.Motor2.setOrientation(QtCore.Qt.Horizontal)
        self.Motor2.setObjectName("Motor2")
        self.S_cal = QtWidgets.QPushButton(self.centralwidget)
        self.S_cal.setGeometry(QtCore.QRect(210, 220, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.S_cal.setFont(font)
        self.S_cal.setObjectName("S_cal")
        self.StopButton = QtWidgets.QPushButton(self.centralwidget)
        self.StopButton.setGeometry(QtCore.QRect(460, 250, 211, 81))
        font = QtGui.QFont()
        font.setPointSize(27)
        self.StopButton.setFont(font)
        self.StopButton.setObjectName("StopButton")
        self.M_cal = QtWidgets.QPushButton(self.centralwidget)
        self.M_cal.setGeometry(QtCore.QRect(210, 280, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.M_cal.setFont(font)
        self.M_cal.setObjectName("M_cal")
        self.H_cal = QtWidgets.QPushButton(self.centralwidget)
        self.H_cal.setGeometry(QtCore.QRect(210, 340, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.H_cal.setFont(font)
        self.H_cal.setObjectName("H_cal")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(59, 200, 121, 201))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.S_button = QtWidgets.QRadioButton(self.groupBox)
        self.S_button.setGeometry(QtCore.QRect(10, 20, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.S_button.setFont(font)
        self.S_button.setObjectName("S_button")
        self.M_button = QtWidgets.QRadioButton(self.groupBox)
        self.M_button.setGeometry(QtCore.QRect(10, 80, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.M_button.setFont(font)
        self.M_button.setObjectName("M_button")
        self.H_button = QtWidgets.QRadioButton(self.groupBox)
        self.H_button.setGeometry(QtCore.QRect(10, 140, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.H_button.setFont(font)
        self.H_button.setObjectName("H_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 760, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.S_cal.setText(_translate("MainWindow", "CALIBRATE"))
        self.StopButton.setText(_translate("MainWindow", "STOP"))
        self.M_cal.setText(_translate("MainWindow", "CALIBRATE"))
        self.H_cal.setText(_translate("MainWindow", "CALIBRATE"))
        self.S_button.setText(_translate("MainWindow", "S"))
        self.M_button.setText(_translate("MainWindow", "M"))
        self.H_button.setText(_translate("MainWindow", "H"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
