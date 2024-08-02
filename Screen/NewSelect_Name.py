import os
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
import threading
from KL_MP_Mix import detect_hand_gestures

class Ui_NewSelectName(QtWidgets.QWidget):
    role_selected = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        self.start_hand_gestures_detection()

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

        self.button1 = self.add_button_with_icon("名稱1", "role1.png")
        self.button2 = self.add_button_with_icon("名稱2", "role2.png")
        self.button3 = self.add_button_with_icon("名稱3", "role3.png")

        self.verticalLayout.addWidget(self.groupBox)
        self.setLayout(self.verticalLayout)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "請選擇團隊名稱"))

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

        # 按下按鈕後攝影機停止
        button.clicked.connect(self.stopCamera)
        button.clicked.connect(lambda: self.role_selected.emit(text))

        return button

    def start_hand_gestures_detection(self):
        threading.Thread(target=self.hand_gestures_detection, daemon=True).start()

    def hand_gestures_detection(self):
        for gesture in detect_hand_gestures():
            self.handle_gesture(gesture)

    # 角色名稱 之後要改成連sql
    def handle_gesture(self, gesture):
        if gesture == '1':
            self.highlight_button(self.button1)
            self.role_selected.emit("名稱1")
        elif gesture == '2':
            self.highlight_button(self.button2)
            self.role_selected.emit("名稱2")
        elif gesture == '3':
            self.highlight_button(self.button3)
            self.role_selected.emit("名稱3")

    def highlight_button(self, button):
        self.reset_button_styles()
        button.setStyleSheet("border: 5px solid red;")

    # 攝影機開啟
    def setupCamera(self):
        self.camera = QtMultimedia.QCamera()
        self.camera.start()
        print("Camera0 started.")

    # 攝影機關閉
    def stopCamera(self):
        if self.camera:
            self.camera.stop()
            print("Camera0 stopped.")

    def reset_button_styles(self):
        self.button1.setStyleSheet("")
        self.button2.setStyleSheet("")
        self.button3.setStyleSheet("")

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
