import threading
import os
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimediaWidgets
from KL_MP_Mix import detect_hand_gestures

class Ui_NewStandBy(QtWidgets.QWidget):
    prevButton_clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.custom_font = self.load_custom_font('C:/Users/julia/AppData/Local/Microsoft/Windows/Fonts/NaikaiFont-Bold.ttf')  # 字體位置
        self.setupUi()
        self.hand_gestures_thread = None
        self.stop_signal = threading.Event()  # 手勢停止
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
        self.title_label.setFont(QtGui.QFont(self.custom_font, 48))  
        self.title_label.setObjectName("title_label")
        self.title_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.verticalLayoutGroupBox.addWidget(self.title_label)

        # 顯示難易度
        self.difficulty_label = QtWidgets.QLabel(self.groupBox)
        self.difficulty_label.setFont(QtGui.QFont(self.custom_font, 32))  
        self.difficulty_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.verticalLayoutGroupBox.addWidget(self.difficulty_label)

        # 攝影機圖框
        self.cameraViewfinder = QtMultimediaWidgets.QCameraViewfinder(self.groupBox)
        self.cameraViewfinder.setObjectName("cameraViewfinder")

        self.mainLayout.addWidget(self.groupBox)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)

        # 上一步 按鈕
        self.prevButton = QtWidgets.QPushButton(self)
        self.prevButton.setFont(QtGui.QFont(self.custom_font, 18)) 
        self.prevButton.setMinimumHeight(100)
        self.prevButton.setFixedWidth(400)
        self.prevButton.setText("上一步")
        self.prevButton.clicked.connect(self.on_prev_clicked)

        # 上一步的圖片
        self.prev_img_label = QtWidgets.QLabel(self)
        img_path_prev = os.path.join(os.path.dirname(__file__), 'img', 'icon5.png')  
        self.prev_img_pixmap = QtGui.QPixmap(img_path_prev)
        self.prev_img_label.setPixmap(self.prev_img_pixmap)
        self.prev_img_label.setFixedSize(200, 200)  
        self.prev_img_label.setScaledContents(True) 

        self.horizontalLayout.addWidget(self.prevButton)
        self.horizontalLayout.addWidget(self.prev_img_label)
        self.horizontalLayout.addStretch()

        # OK 按鈕
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setFont(QtGui.QFont(self.custom_font, 18))  
        self.pushButton.setMinimumHeight(100)
        self.pushButton.setFixedWidth(400)
        self.pushButton.setText("OK")
        self.pushButton.clicked.connect(self.close)  # 執行後關閉頁面

        # OK的圖片
        self.ok_img_label = QtWidgets.QLabel(self)
        img_path_ok = os.path.join(os.path.dirname(__file__), 'img', 'icon6.png')  
        self.ok_img_pixmap = QtGui.QPixmap(img_path_ok)
        self.ok_img_label.setPixmap(self.ok_img_pixmap)
        self.ok_img_label.setFixedSize(200, 200)  
        self.ok_img_label.setScaledContents(True)

        centerSpacer = QtWidgets.QSpacerItem(60, 60, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(centerSpacer)
        self.horizontalLayout.addWidget(self.pushButton)
        self.horizontalLayout.addWidget(self.ok_img_label)

        rightSpacer = QtWidgets.QSpacerItem(60, 60, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(rightSpacer)
        self.mainLayout.addLayout(self.horizontalLayout)

        bottomSpacer = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.mainLayout.addItem(bottomSpacer)
        
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

    # 上一頁的難易度
    def set_difficulty(self, difficulty):
        print(f"Setting difficulty: {difficulty}") 
        self.difficulty_label.setText(f"難易度: {difficulty}")

    # 上一步
    def on_prev_clicked(self):
        self.prevButton_clicked.emit()

    # 字體
    def load_custom_font(self, font_path):
        if not os.path.exists(font_path):
            print(f"字體文件不存在: {font_path}")
            return "標楷體"  # 如果字體文件不存在，返回標楷體作為後備字體
        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print("字體加載失敗！")
            return "標楷體"  # 如果加載失敗，返回標楷體
        font_families = QtGui.QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            font_family = font_families[0]
            print(f"成功加載字體-4: {font_family}")
            return font_family  # 成功加載字體
        else:
            print("未找到字體名稱")
            return "標楷體"  # 未找到字體名稱時，返回標楷體

    # 手勢開始
    def start_hand_gestures_detection(self):
        self.stop_signal.clear()  
        if self.hand_gestures_thread is None or not self.hand_gestures_thread.is_alive():
            self.hand_gestures_thread = threading.Thread(target=self.hand_gestures_detection, daemon=True)
            self.hand_gestures_thread.start()

    # 手勢停止
    def stop_hand_gestures_detection(self):
        if self.hand_gestures_thread is not None and self.hand_gestures_thread.is_alive():
            self.stop_signal.set()  

    def hand_gestures_detection(self):
        for gesture in detect_hand_gestures():
            if self.stop_signal.is_set():  # 檢查要不要停止
                break
            self.handle_gesture(gesture)

    # 按鈕手勢對比
    def handle_gesture(self, gesture):
        print(f"Detected gesture: {gesture}")
        if gesture == 'back':
            self.highlight_button(self.prevButton)
            self.on_prev_clicked()
            self.stop_signal.set()
        elif gesture == 'ok':
            self.highlight_button(self.pushButton)
            self.stop_signal.set()
            self.close()  # 關閉整個頁面

    # 按鈕的紅框
    def highlight_button(self, button):
        self.reset_button_styles()  # 清除樣式
        button.setStyleSheet("border: 5px solid red;")  

    # 點選到其他的按鈕會切換紅框
    def reset_button_styles(self):
        self.prevButton.setStyleSheet("")  
        self.pushButton.setStyleSheet("")

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
