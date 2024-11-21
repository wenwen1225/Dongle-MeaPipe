import os
import random
import threading
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from KL_MP_Mix import detect_hand_gestures

class Ui_NewSelectName(QtWidgets.QWidget):
    role_selected = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.hand_gestures_thread = None
        self.stop_signal = threading.Event()  
        self.timer = None
        self.button_texts = self.load_button_texts('Data/camp.txt')  # 團隊名稱txt檔
        self.custom_font = self.load_custom_font('Font\\NaikaiFont-Bold.ttf') # 字體位置
        self.media_player = QMediaPlayer()  # 初始化媒體播放器
        self.setupUi()
        self.schedule_sound_playback()  # 計畫聲音播放

    def setupUi(self):
        self.setObjectName("MainWindow")
        screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
        self.setGeometry(screen_geometry)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        # 使用垂直布局並讓其填滿空間
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)  # 邊界

        # 請選擇團隊名稱 標題
        self.label = QtWidgets.QLabel(self.centralwidget)
        if self.custom_font:  # 如果字體顯示成功，使用該字體
            font = QtGui.QFont(self.custom_font, 48)
            self.label.setFont(font)
        else:
            self.label.setFont(QtGui.QFont("標楷體", 48))  
        self.label.setObjectName("label")
        self.label.setAlignment(QtCore.Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.label)

        # 簡單文字+圖片 說明
        self.gesture_label = QtWidgets.QLabel(self.centralwidget)
        if self.custom_font:
            font = QtGui.QFont(self.custom_font, 24)
            self.gesture_label.setFont(font)
        else:
            self.gesture_label.setFont(QtGui.QFont("標楷體", 24))
        self.gesture_label.setAlignment(QtCore.Qt.AlignCenter)

        gesture_text = '<p>請比出手勢'
        gesture_image_filenames = [f'icon{i}.png' for i in range(1, 4)]

        for filename in gesture_image_filenames:
            img_path = os.path.join(os.path.dirname(__file__), 'img', filename)
            gesture_text += f' <img src="{img_path}" width="150"/>'  # 圖片大小
        gesture_text += ' 來進行選擇團隊名稱!</p>'

        self.gesture_label.setText(gesture_text)
        self.verticalLayout.addWidget(self.gesture_label)

        # 初始化 groupBox
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setStyleSheet("QGroupBox { border: none; }")
        self.groupBox.setTitle("")

        self.verticalLayoutGroupBox = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayoutGroupBox.setObjectName("verticalLayoutGroupBox")

        spacer = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer)

        # 團隊按鈕，依照 camp.txt 中的文字
        if len(self.button_texts) >= 3:
            img_folder = os.path.join(os.path.dirname(__file__), 'img')  # 圖片資料夾
            available_images = [f for f in os.listdir(img_folder) if 'role' in f and f.endswith(('.png', '.jpg', '.jpeg'))]
            selected_images = random.sample(available_images, 3)  # 隨機選取 3 張不重複的圖片
            selected_texts = random.sample(self.button_texts, 3)  # 隨機選擇 3 行不重複的文字

            self.button1 = self.add_button_with_icon(selected_texts[0], selected_images[0])
            self.button2 = self.add_button_with_icon(selected_texts[1], selected_images[1])
            self.button3 = self.add_button_with_icon(selected_texts[2], selected_images[2])
        else:
            print("camp.txt 文件中需要至少有 3 行文字")

        self.verticalLayout.addWidget(self.groupBox)
        self.setLayout(self.verticalLayout)

        self.retranslateUi()

    # 設定聲音播放計畫
    def schedule_sound_playback(self):
        QTimer.singleShot(2000, self.play_sound)  # 2 秒後執行 play_sound

    # 播放聲音的方法
    def play_sound(self):
        mp3_path = os.path.join(os.path.dirname(__file__), 'sound', 'Select_Name_sound.mp3')  # MP3 文件路徑
        if not os.path.exists(mp3_path):
            print(f"MP3 檔案不存在: {mp3_path}")
            return
        
        url = QUrl.fromLocalFile(mp3_path)
        content = QMediaContent(url)
        self.media_player.setMedia(content)
        self.media_player.setVolume(70)  # 設置音量，範圍 0-100
        self.media_player.play()

    # 標題
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "請選擇團隊名稱"))

    # 按鈕+圖片
    def add_button_with_icon(self, text, icon_filename):
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignCenter)

        button = QtWidgets.QPushButton(text, self.groupBox)
        if self.custom_font:
            font = QtGui.QFont(self.custom_font, 30)
            button.setFont(font)
        else:
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
        button.clicked.connect(lambda: self.role_selected.emit(text))  
        return button
    
    # 讀取txt的內容
    def load_button_texts(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return [line.strip() for line in lines if line.strip()]
    
    # 字體
    def load_custom_font(self, font_path):
        if not os.path.exists(font_path):
            print(f"字體文件不存在: {font_path}")
            return None
        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print("字體加載失敗！")
            return None
        font_families = QtGui.QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            font_family = font_families[0]
            print(f"成功加載字體-1: {font_family}")
            return font_family  
        else:
            print("未找到字體名稱")
            return None

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
        self.cancel_timer()  # 取消計時器

    def hand_gestures_detection(self):
        for gesture in detect_hand_gestures():
            if self.stop_signal.is_set():  # 檢查要不要停止
                break
            self.handle_gesture(gesture)

    # 按鈕手勢對比
    def handle_gesture(self, gesture):
        print(f"Detected gesture: {gesture}")  # 測試是否抓到手勢
        if gesture == '1':
            self.highlight_button(self.button1)
            threading.Timer(3, self.execute_button_action, args=(self.button1.text(),)).start()
            self.stop_signal.set()  
        elif gesture == '2':
            self.highlight_button(self.button2)
            threading.Timer(3, self.execute_button_action, args=(self.button2.text(),)).start()
            self.stop_signal.set() 
        elif gesture == '3':
            self.highlight_button(self.button3)
            threading.Timer(3, self.execute_button_action, args=(self.button3.text(),)).start()
            self.stop_signal.set()  

    def execute_button_action(self, button_text):
        print(f"執行按鈕的動作: {button_text}")
        self.role_selected.emit(button_text)

    # 計時器開始
    def start_timer(self, button_text):
        self.cancel_timer()  
        self.timer = threading.Timer(3, self.execute_button_action, args=(button_text,))
        self.timer.start()

    # 取消計時器
    def cancel_timer(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None  # 重置計時器

    # 按鈕的紅框
    def highlight_button(self, button):
        self.reset_button_styles()  # 清除樣式
        button.setStyleSheet("border: 5px solid red;")  

    # 點選到其他的按鈕會切換紅框
    def reset_button_styles(self):
        self.button1.setStyleSheet("")  
        self.button2.setStyleSheet("")
        self.button3.setStyleSheet("")

    # 關閉資訊
    def closeEvent(self, event):
        self.stop_hand_gestures_detection()  # 停止手勢檢測
        event.accept()  # 確保關閉事件被接受

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