from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimediaWidgets, QtMultimedia

class Ui_NewStandBy(QtWidgets.QWidget):
    prevButton_clicked = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setObjectName("MainWindow")
        self.setGeometry(QtWidgets.QApplication.desktop().availableGeometry())

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)

        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setStyleSheet("QGroupBox { border: none; }")  
        self.groupBox.setTitle("")  

        self.verticalLayoutGroupBox = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayoutGroupBox.setObjectName("verticalLayoutGroupBox")

        # 請玩家站定位 標題
        self.title_label = QtWidgets.QLabel(self.groupBox)
        self.title_label.setFont(QtGui.QFont("標楷體", 48))
        self.title_label.setObjectName("title_label")
        self.title_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.verticalLayoutGroupBox.addWidget(self.title_label)

        # 難易度
        self.difficulty_label = QtWidgets.QLabel(self.groupBox)
        self.difficulty_label.setFont(QtGui.QFont("標楷體", 24))
        self.difficulty_label.setObjectName("difficulty_label")
        self.difficulty_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.verticalLayoutGroupBox.addWidget(self.difficulty_label, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # 攝影機框
        self.cameraViewfinder = QtMultimediaWidgets.QCameraViewfinder(self.groupBox)
        self.cameraViewfinder.setObjectName("cameraViewfinder")
        self.verticalLayoutGroupBox.addWidget(self.cameraViewfinder)

        # 上一步
        self.prevButton = QtWidgets.QPushButton(self.groupBox)
        self.prevButton.setFont(QtGui.QFont("標楷體", 18))
        self.prevButton.setMinimumHeight(100)
        self.prevButton.setFixedWidth(400)  
        self.verticalLayoutGroupBox.addWidget(self.prevButton, alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft)
        self.prevButton.clicked.connect(self.on_prev_clicked)

        self.verticalLayout.addWidget(self.groupBox)

        # OK按鈕
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setFont(QtGui.QFont("標楷體", 24))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.close)  # 按下關閉視窗
        self.verticalLayout.addWidget(self.pushButton, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)

        self.setupCamera()  # 使用攝影機
        self.retranslateUi()

    # 文字顯示
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.title_label.setText(_translate("MainWindow", "請玩家站定位"))
        self.prevButton.setText(_translate("MainWindow", "上一步"))
        self.pushButton.setText(_translate("MainWindow", "OK"))

    # 上一頁的難易度
    def set_difficulty(self, difficulty):
        self.difficulty_label.setText(f"難易度: {difficulty}")

    # 上一步
    def on_prev_clicked(self):
        self.prevButton_clicked.emit()

    # 攝影機
    def setupCamera(self):
        self.camera = QtMultimedia.QCamera()
        self.camera.setViewfinder(self.cameraViewfinder)
        self.camera.start() #開啟
        print("Camera started.")

    # 關閉攝影機
    def stopCamera(self):
        if self.camera:
            self.camera.stop()
            print("Camera stopped.")

    # 關閉程式
    def closeEvent(self, event):
        self.stopCamera()  # 停止攝影機
        event.accept()  # 允許關閉事件
        QtWidgets.QApplication.quit()  # 關閉應用程式

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Ui_NewStandBy()
    mainWindow.show()
    sys.exit(app.exec_())
