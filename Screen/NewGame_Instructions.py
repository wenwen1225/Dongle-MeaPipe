from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
import threading
from KL_MP_Mix import detect_hand_gestures

class Ui_NewGameInstructions(QtWidgets.QWidget):
    nextButton_clicked = QtCore.pyqtSignal()
    prevButton_clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        #self.camera = None
        self.hand_gestures_thread = None
        self.stop_signal = threading.Event()  #  手勢停止

    def setupUi(self):
        self.setObjectName("MainWindow")
        screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
        self.setGeometry(screen_geometry)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setStyleSheet("QGroupBox { border: none; }")
        self.groupBox.setTitle("")

        self.verticalLayoutGroupBox = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayoutGroupBox.setObjectName("verticalLayoutGroupBox")

        # 遊戲規則說明
        self.label = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont("標楷體", 48)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayoutGroupBox.addWidget(self.label)

        # 團隊名稱
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont("標楷體", 25)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayoutGroupBox.addWidget(self.label_5)

        # 說明
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont("標楷體", 25)
        self.label_2.setFont(font)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayoutGroupBox.addWidget(self.label_2)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        # 上一步
        self.prevButton = QtWidgets.QPushButton(self.groupBox)
        self.prevButton.setObjectName("prevButton")
        self.prevButton.setFont(QtGui.QFont("標楷體", 18))
        self.prevButton.setMinimumHeight(100)
        self.horizontalLayout.addWidget(self.prevButton)

        # 說明
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont("標楷體", 25)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)

        # 箭頭
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont("標楷體", 90)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3, alignment=QtCore.Qt.AlignCenter)

        # 下一步
        self.nextButton = QtWidgets.QPushButton(self.groupBox)
        self.nextButton.setObjectName("pushButton")
        self.nextButton.setFont(QtGui.QFont("標楷體", 18))
        self.nextButton.setMinimumHeight(100)
        self.horizontalLayout.addWidget(self.nextButton)

        self.verticalLayoutGroupBox.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.groupBox)

        self.setLayout(self.verticalLayout)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.nextButton.clicked.connect(self.on_next_clicked)
        self.prevButton.clicked.connect(self.on_prev_clicked)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "遊戲規則說明"))
        self.label_2.setText(_translate("MainWindow", "確定完營隊名稱後，進行難易度選擇，選擇完畢請玩家站到指定位子，遊戲開始會出現題目，請從四字成語中找到一個錯誤的字，並舉出指定手勢確定答案，計時2分鐘答題，答題越多分數越高，答錯超過3次遊戲失敗，直接計算分數，請各位玩家加油拿到高分!"))
        self.nextButton.setText(_translate("MainWindow", "下一步"))
        self.prevButton.setText(_translate("MainWindow", "上一步"))
        self.label_3.setText(_translate("MainWindow", "→"))
        self.label_4.setText(_translate("MainWindow", "閱讀完畢後請按下一步開始遊戲!"))

    # 下一步
    def on_next_clicked(self):
        self.nextButton_clicked.emit()

    # 前一步
    def on_prev_clicked(self):
        self.prevButton_clicked.emit()

    # 上一頁的團隊名稱
    def set_team_name(self, team_name):
        self.label_5.setText(f"團隊名稱: {team_name}")

    # 手勢開始
    def start_hand_gestures_detection(self):
        self.stop_signal.clear()  # 清除資料
        #self.setupCamera()
        self.hand_gestures_thread = threading.Thread(target=self.hand_gestures_detection, daemon=True)
        self.hand_gestures_thread.start()

    # 手勢停止
    def stop_hand_gestures_detection(self):
        if self.hand_gestures_thread is not None:
            self.stop_signal.set()
            self.hand_gestures_thread.join() 

    def hand_gestures_detection(self):
        for gesture in detect_hand_gestures():
            if self.stop_signal.is_set():  # 檢查要不要停止
                break
            self.handle_gesture(gesture)

    # 按鈕手勢對比
    def handle_gesture(self, gesture):
        print(f"Detected-1 gesture: {gesture}")
        if gesture == 'back':
            self.on_prev_clicked()
            self.stop_signal.set()
        elif gesture == 'ok':
            self.on_next_clicked()
            self.stop_signal.set()

    # 關閉資訊
    def closeEvent(self, event):
        self.stop_hand_gestures_detection()
        super().closeEvent(event)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_NewGameInstructions()
    MainWindow.setCentralWidget(ui)

    window_rect = MainWindow.frameGeometry()
    center_point = QtWidgets.QDesktopWidget().availableGeometry().center()
    window_rect.moveCenter(center_point)
    MainWindow.move(window_rect.topLeft())

    MainWindow.show()
    sys.exit(app.exec_())
