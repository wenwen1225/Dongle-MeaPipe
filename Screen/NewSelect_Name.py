import os
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
import threading
from KL_MP_Mix import detect_hand_gestures

class Ui_NewSelectName(QtWidgets.QWidget):
    role_selected = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        self.camera = None
        self.hand_gestures_thread = None
        self.stop_signal = threading.Event()  # 手勢停止

    def setupUi(self):
        self.setObjectName("MainWindow")
        screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
        self.setGeometry(screen_geometry)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setFont(QtGui.QFont("標楷體", 48))
        self.label.setObjectName("label")
        self.label.setAlignment(QtCore.Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.label)

        spacer = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer)

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setStyleSheet("QGroupBox { border: none; }")
        self.groupBox.setTitle("")

        self.verticalLayoutGroupBox = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayoutGroupBox.setObjectName("verticalLayoutGroupBox")

        # 團隊按鈕，之後連資料庫
        self.button1 = self.add_button_with_icon("名稱1", "role1.png")
        self.button2 = self.add_button_with_icon("名稱2", "role2.png")
        self.button3 = self.add_button_with_icon("名稱3", "role3.png")

        self.verticalLayout.addWidget(self.groupBox)
        self.setLayout(self.verticalLayout)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "請選擇團隊名稱"))

    # 按鈕+圖片
    def add_button_with_icon(self, text, icon_filename):
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignCenter)

        button = QtWidgets.QPushButton(text, self.groupBox)
        button.setFont(QtGui.QFont("標楷體", 30))
        button.setMinimumHeight(200)
        button.setFixedWidth(400)

        img_path = os.path.join(os.path.dirname(__file__), 'img', icon_filename)
        pixmap = QtGui.QPixmap(img_path)
        icon_label = QtWidgets.QLabel()
        icon_label.setPixmap(pixmap)
        icon_label.setFixedSize(200, 200)
        icon_label.setScaledContents(True)

        button_layout.addWidget(icon_label)
        button_layout.addWidget(button)

        self.verticalLayoutGroupBox.addLayout(button_layout)
        button.clicked.connect(lambda: self.role_selected.emit(text))  # emit signal only
        return button
    
    # 手勢開始
    def start_hand_gestures_detection(self):
        self.stop_signal.clear()  # 清除資料
        self.setupCamera()
        self.hand_gestures_thread = threading.Thread(target=self.hand_gestures_detection, daemon=True)
        self.hand_gestures_thread.start()

    def hand_gestures_detection(self):
        for gesture in detect_hand_gestures():
            if self.stop_signal.is_set():  # 檢查要不要停止
                break
            self.handle_gesture(gesture)
            #self.gesture_detected.emit(gesture) 
            
    # 按鈕手勢比對        
    def handle_gesture(self, gesture):
        print(f"Detected-0 gesture: {gesture}") # 測試有沒有抓到手勢
        if gesture == '1':
            self.highlight_button(self.button1)
            self.role_selected.emit("名稱1")
            self.stop_signal.set()
        elif gesture == '2':
            self.highlight_button(self.button2)
            self.role_selected.emit("名稱2")
            self.stop_signal.set()
        elif gesture == '3':
            self.highlight_button(self.button3)
            self.role_selected.emit("名稱3")
            self.stop_signal.set()

    # 按鈕的紅框
    def highlight_button(self, button):
        self.reset_button_styles()
        button.setStyleSheet("border: 5px solid red;")

    # 取消紅框 還未用好?
    def reset_button_styles(self):
        self.button1.setStyleSheet("")
        self.button2.setStyleSheet("")
        self.button3.setStyleSheet("")

    # 開啟攝影機
    def setupCamera(self):
        if self.camera is None:
            self.camera = QtMultimedia.QCamera()
            self.camera.start()
            print("Camera0 started.")

    # 關閉攝影機
    def stopCamera(self):
        if self.camera is not None:
            self.camera.stop()
            print("Camera0 stopped.")
            self.camera = None

    # 關閉資訊
    def closeEvent(self, event):
        self.stopCamera()
        if self.hand_gestures_thread is not None:
            self.stop_signal.set()  
            self.hand_gestures_thread.join()  
        super().closeEvent(event)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_NewSelectName()
    MainWindow.setCentralWidget(ui)

    window_rect = MainWindow.frameGeometry()
    center_point = QtWidgets.QDesktopWidget().availableGeometry().center()
    window_rect.moveCenter(center_point)
    MainWindow.move(window_rect.topLeft())

    MainWindow.show()
    sys.exit(app.exec_())
