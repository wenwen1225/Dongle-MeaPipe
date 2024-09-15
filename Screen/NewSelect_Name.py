import os
import random
import threading
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtCore import Qt
from KL_MP_Mix import detect_hand_gestures

class Ui_NewSelectName(QtWidgets.QWidget):
    role_selected = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.hand_gestures_thread = None
        self.stop_signal = threading.Event()  # 手勢停止
        self.button_texts = self.load_button_texts('C:\\mypython4\\pack\\Data\\camp.txt')
        self.setupUi()

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

        # 團隊按鈕，依照 camp.txt 中的文字
        if len(self.button_texts) >= 3:
            icon_paths = ['role1.png', 'role2.png', 'role3.png']
            selected_texts = random.sample(self.button_texts, 3)  # 隨機選擇 3 行文字

            self.button1 = self.add_button_with_icon(selected_texts[0], icon_paths[0])
            self.button2 = self.add_button_with_icon(selected_texts[1], icon_paths[1])
            self.button3 = self.add_button_with_icon(selected_texts[2], icon_paths[2])
        else:
            print("camp.txt 文件中需要至少有 3 行文字")

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
    
    def load_button_texts(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        # 移除空行並返回文本列表
        return [line.strip() for line in lines if line.strip()]

    # 手勢開始
    def start_hand_gestures_detection(self):
        self.stop_signal.clear()  # 清除資料
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
            
    # 按鈕手勢比對        
    def handle_gesture(self, gesture):
        print(f"Detected-0 gesture: {gesture}") # 測試有沒有抓到手勢
        if gesture == '1':
            self.highlight_button(self.button1)
            self.role_selected.emit(self.button1.text())
            self.stop_signal.set()
        elif gesture == '2':
            self.highlight_button(self.button2)
            self.role_selected.emit(self.button2.text())
            self.stop_signal.set()
        elif gesture == '3':
            self.highlight_button(self.button3)
            self.role_selected.emit(self.button3.text())
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

    # 關閉資訊
    def closeEvent(self, event):
        #self.stopCamera()
        if self.hand_gestures_thread is not None:
            self.stop_signal.set()  
            self.hand_gestures_thread.join()  

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
