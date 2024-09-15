import threading
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimediaWidgets
from KL_MP_Mix import detect_hand_gestures

class Ui_NewStandBy(QtWidgets.QWidget):
    prevButton_clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.setupUi()
        self.hand_gestures_thread = None
        self.stop_signal = threading.Event()  # 手势停止信号
        self.cameraViewfinder = None  

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setGeometry(QtWidgets.QApplication.desktop().availableGeometry())

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setObjectName("mainLayout")
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setStyleSheet("QGroupBox { border: none; }")
        self.groupBox.setTitle("")  

        self.verticalLayoutGroupBox = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayoutGroupBox.setObjectName("verticalLayoutGroupBox")
        self.verticalLayoutGroupBox.setAlignment(QtCore.Qt.AlignCenter)

        # 請玩家站定位-標題
        self.title_label = QtWidgets.QLabel(self.groupBox)
        self.title_label.setFont(QtGui.QFont("標楷體", 48))
        self.title_label.setObjectName("title_label")
        self.title_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.verticalLayoutGroupBox.addWidget(self.title_label)

        # 顯示難易度
        self.difficulty_label = QtWidgets.QLabel(self.groupBox)
        self.difficulty_label.setFont(QtGui.QFont("標楷體", 32))
        self.difficulty_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.verticalLayoutGroupBox.addWidget(self.difficulty_label)

        # 攝影機圖框
        self.cameraViewfinder = QtMultimediaWidgets.QCameraViewfinder(self.groupBox)
        self.cameraViewfinder.setObjectName("cameraViewfinder")
        self.cameraViewfinder.setMinimumSize(1200, 800)  # 设置摄像头框的大小

        self.mainLayout.addWidget(self.groupBox)

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")
        self.buttonLayout.setAlignment(QtCore.Qt.AlignHCenter)

        # 上一步
        self.prevButton = QtWidgets.QPushButton(self)
        self.prevButton.setFont(QtGui.QFont("標楷體", 18))
        self.prevButton.setMinimumHeight(100)
        self.prevButton.setFixedWidth(200)
        self.prevButton.setText("上一步")
        self.prevButton.clicked.connect(self.on_prev_clicked)
        self.buttonLayout.addWidget(self.prevButton)

        # OK按鈕
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setFont(QtGui.QFont("標楷體", 18))
        self.pushButton.setMinimumHeight(100)
        self.pushButton.setFixedWidth(200)
        self.pushButton.setText("OK")
        self.pushButton.clicked.connect(self.close)  # 按下关闭窗口
        self.buttonLayout.addWidget(self.pushButton)

        self.mainLayout.addLayout(self.buttonLayout)
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.title_label.setText(_translate("MainWindow", "請玩家站定位"))

    def set_camera_viewfinder(self, camera_viewfinder):
        if self.cameraViewfinder:
            self.cameraViewfinder.setParent(None)  
        if camera_viewfinder:
            self.verticalLayoutGroupBox.addWidget(camera_viewfinder)  
            camera_viewfinder.show()  
        self.cameraViewfinder = camera_viewfinder
        print("Camera viewfinder set in NewStandBy.")

    def set_difficulty(self, difficulty):
        print(f"Setting difficulty: {difficulty}") 
        self.difficulty_label.setText(f"難易度: {difficulty}")

    def on_prev_clicked(self):
        self.prevButton_clicked.emit()

    def start_hand_gestures_detection(self):
        self.stop_signal.clear()  
        if self.hand_gestures_thread is None or not self.hand_gestures_thread.is_alive():
            self.hand_gestures_thread = threading.Thread(target=self.hand_gestures_detection, daemon=True)
            self.hand_gestures_thread.start()

    def stop_hand_gestures_detection(self):
        if self.hand_gestures_thread is not None and self.hand_gestures_thread.is_alive():
            self.stop_signal.set()  

    def hand_gestures_detection(self):
        for gesture in detect_hand_gestures():
            if self.stop_signal.is_set():  # 檢查要不要停止
                break
            self.handle_gesture(gesture)

    def handle_gesture(self, gesture):
        print(f"Detected gesture: {gesture}")
        if gesture == 'back':
            self.on_prev_clicked()
            self.stop_signal.set()
        elif gesture == 'ok':
            self.stop_signal.set()
            self.close()  # 關閉整個頁面

    def closeEvent(self, event):
        self.stop_hand_gestures_detection()  
        if self.cameraViewfinder:
            self.cameraViewfinder.setParent(None)  

        # 關閉所有視窗
        for widget in QtWidgets.QApplication.topLevelWidgets():
            if widget is not self and isinstance(widget, QtWidgets.QWidget):
                widget.close()

        event.accept()  # 關閉事件

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_NewStandBy()
    MainWindow.setCentralWidget(ui)
    
    MainWindow.show()
    sys.exit(app.exec_())
