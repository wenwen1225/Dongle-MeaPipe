from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
import os
import threading
from KL_MP_Mix import detect_hand_gestures

class Ui_NewGameInstructions(QtWidgets.QWidget):
    nextButton_clicked = QtCore.pyqtSignal()
    prevButton_clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.hand_gestures_thread = None
        self.stop_signal = threading.Event()  # 手勢停止
        self.custom_font = self.load_custom_font('C:/Users/julia/AppData/Local/Microsoft/Windows/Fonts/NaikaiFont-Bold.ttf')  # 字體位置
        self.setupUi()

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

        # 遊戲規則說明 標題
        self.label = QtWidgets.QLabel(self.groupBox)
        if self.custom_font:  # 如果字體顯示成功，使用該字體
            font = QtGui.QFont(self.custom_font, 48)
            self.label.setFont(font)
        else:
            self.label.setFont(QtGui.QFont("標楷體", 48))  
        self.label.setObjectName("label")
        self.verticalLayoutGroupBox.addWidget(self.label)
        self.label.setAlignment(QtCore.Qt.AlignCenter)  # 置中對齊
        self.verticalLayoutGroupBox.addWidget(self.label)

        # 團隊名稱
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        if self.custom_font:  # 如果字體顯示成功，使用該字體
            font = QtGui.QFont(self.custom_font, 25)
            self.label_5.setFont(font)
        else:
            self.label_5.setFont(QtGui.QFont("標楷體", 25))  
        self.label_5.setObjectName("label_5")
        self.verticalLayoutGroupBox.addWidget(self.label_5)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)  # 置中對齊
        self.verticalLayoutGroupBox.addWidget(self.label_5)

        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayoutGroupBox.addItem(spacerItem)

        # 影片撥放組件
        self.video_player = QtMultimediaWidgets.QVideoWidget(self.centralwidget)
        self.video_player.setMinimumSize(800, 600)  # 影片尺寸
        self.video_player.setObjectName("video_player")
        self.verticalLayoutGroupBox.addWidget(self.video_player)  

        # 創建 QMediaPlayer
        self.media_player = QtMultimedia.QMediaPlayer(self)
        self.media_player.setVideoOutput(self.video_player)

        # 影片路徑
        video_path = 'C:/mypython4/pack/Screen/game_video.mp4'  
        if not os.path.exists(video_path):
            print(f"影片文件不存在: {video_path}")
        else:
            self.media_player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(video_path)))
            self.media_player.play()

        # 說明
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        if self.custom_font:  # 如果字體加載成功，使用該字體
            font = QtGui.QFont(self.custom_font, 25)
            self.label_2.setFont(font)
        else:
            self.label_2.setFont(QtGui.QFont("標楷體", 25))  
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayoutGroupBox.addWidget(self.label_2)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        # 上一步
        self.prevButton = QtWidgets.QPushButton(self.groupBox)
        self.prevButton.setObjectName("prevButton")
        self.prevButton.setFont(QtGui.QFont(self.custom_font if self.custom_font else "標楷體", 18))
        self.prevButton.setMinimumHeight(100)

        # 上一步的圖片
        self.prev_img_label = QtWidgets.QLabel(self.groupBox)
        img_path_prev = os.path.join(os.path.dirname(__file__), 'img', 'icon5.png')  
        self.prev_img_pixmap = QtGui.QPixmap(img_path_prev)
        self.prev_img_label.setPixmap(self.prev_img_pixmap)
        self.prev_img_label.setFixedSize(300, 300)  
        self.prev_img_label.setScaledContents(True) 

        self.horizontalLayout.addWidget(self.prevButton)
        self.horizontalLayout.addWidget(self.prev_img_label)

        # 說明
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        if self.custom_font:  # 如果字體顯示成功，使用該字體
            font = QtGui.QFont(self.custom_font, 25)
            self.label_4.setFont(font)
        else:
            self.label_4.setFont(QtGui.QFont("標楷體", 25))  
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)

        # 箭頭
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont(self.custom_font if self.custom_font else "標楷體", 90)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3, alignment=QtCore.Qt.AlignCenter)

        # 下一步
        self.nextButton = QtWidgets.QPushButton(self.groupBox)
        self.nextButton.setObjectName("pushButton")
        self.nextButton.setFont(QtGui.QFont(self.custom_font if self.custom_font else "標楷體", 18))
        self.nextButton.setMinimumHeight(100)

        # 下一步的圖片
        self.next_img_label = QtWidgets.QLabel(self.groupBox)
        img_path_next = os.path.join(os.path.dirname(__file__), 'img', 'icon6.png') 
        self.next_img_pixmap = QtGui.QPixmap(img_path_next)
        self.next_img_label.setPixmap(self.next_img_pixmap)
        self.next_img_label.setFixedSize(200, 200) 
        self.next_img_label.setScaledContents(True)

        self.horizontalLayout.addWidget(self.nextButton)
        self.horizontalLayout.addWidget(self.next_img_label)

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
        self.nextButton.setText(_translate("MainWindow", "下一步"))
        self.prevButton.setText(_translate("MainWindow", "上一步"))
        self.label_3.setText(_translate("MainWindow", "→"))
        self.label_4.setText(_translate("MainWindow", "閱讀完畢後請按下一步開始遊戲!"))

    # 下一步
    def on_next_clicked(self):
        self.nextButton_clicked.emit()
        self.media_player.pause()  # 暫停影片

    # 上一步
    def on_prev_clicked(self):
        self.prevButton_clicked.emit()
        self.media_player.pause()  # 暫停影片

    # 上一頁的團隊名稱
    def set_team_name(self, team_name):
        self.label_5.setText(f"團隊名稱: {team_name}")

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
            print(f"成功加載字體-2: {font_family}")
            return font_family  # 成功加載字體
        else:
            print("未找到字體名稱")
            return "標楷體"  # 未找到字體名稱時，返回標楷體

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

    # 按鈕手勢對比
    def handle_gesture(self, gesture):
        print(f"Detected gesture: {gesture}")
        if gesture == 'back':
            self.highlight_button(self.prevButton)
            self.on_prev_clicked()
            self.stop_signal.set()
        elif gesture == 'ok':
            self.highlight_button(self.nextButton)
            self.on_next_clicked()
            self.stop_signal.set()

    # 按鈕的紅框
    def highlight_button(self, button):
        self.reset_button_styles()  # 清除樣式
        button.setStyleSheet("border: 5px solid red;")  

    # 點選到其他的按鈕會切換紅框
    def reset_button_styles(self):
        self.prevButton.setStyleSheet("")
        self.nextButton.setStyleSheet("")

    # 關閉資訊
    def closeEvent(self, event):
        self.stop_hand_gestures_detection()
        self.media_player.stop()  # 停止影片
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
