import threading
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimediaWidgets, QtMultimedia
from KL_MP_Mix import detect_hand_gestures  

class Ui_NewStandBy(QtWidgets.QWidget):
    prevButton_clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.setupUi()
        self.camera = None
        self.hand_gestures_thread = None
        self.stop_signal = threading.Event()  #  手勢停止

    def setupUi(self):
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

        # 請玩家站定位-標題
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

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.title_label.setText(_translate("MainWindow", "請玩家站定位"))
        self.prevButton.setText(_translate("MainWindow", "上一步"))
        self.pushButton.setText(_translate("MainWindow", "OK"))

    def set_difficulty(self, difficulty):
        self.difficulty_label.setText(f"難易度: {difficulty}")

    def on_prev_clicked(self):
        self.prevButton_clicked.emit()

    def start_hand_gestures_detection(self):
        self.stop_signal.clear()  # 确保停止信号被清除
        self.setupCamera()
        if self.hand_gestures_thread is None or not self.hand_gestures_thread.is_alive():
            self.hand_gestures_thread = threading.Thread(target=self.hand_gestures_detection, daemon=True)
            self.hand_gestures_thread.start()

    def stop_hand_gestures_detection(self):
        if self.hand_gestures_thread is not None and self.hand_gestures_thread.is_alive():
            self.stop_signal.set()  # 设置停止信号
            #self.hand_gestures_thread.join()  # 等待手势检测线程结束

    def hand_gestures_detection(self):
        for gesture in detect_hand_gestures():
            if self.stop_signal.is_set():  # 检查是否需要停止
                break
            self.handle_gesture(gesture)

    def handle_gesture(self, gesture):
        print(f"Detected-3 gesture: {gesture}")
        if gesture == 'back':
            self.on_prev_clicked()
            self.stop_signal.set()
        elif gesture == 'ok':
            self.closeEvent(QtGui.QCloseEvent())

    def setupCamera(self):
        self.camera = QtMultimedia.QCamera()
        self.camera.setViewfinder(self.cameraViewfinder)
        self.camera.start()  # 开启摄像机
        print("Camera3 started.")

    def stopCamera(self):
        if self.camera:
            self.camera.stop()
            print("Camera3 stopped.")
            self.camera = None

    def closeEvent(self, event):
        self.stopCamera()  # 停止摄像机
        self.stop_hand_gestures_detection()  # 停止手势检测
        event.accept()  # 允许关闭事件
        QtWidgets.QApplication.quit()  # 关闭应用程序

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_NewStandBy()
    MainWindow.setCentralWidget(ui)
    
    MainWindow.show()
    sys.exit(app.exec_())
