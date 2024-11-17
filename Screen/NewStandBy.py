import threading
import os
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimediaWidgets
from PyQt5.QtMultimedia import QCamera, QCameraInfo
from KL_MP_Mix import detect_hand_gestures

class Ui_NewStandBy(QtWidgets.QWidget):
    prevButton_clicked = QtCore.pyqtSignal()
    pushButton_clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.custom_font = self.load_custom_font('Font\\NaikaiFont-Bold.ttf')  # 字体位置
        self.setupUi()
        self.hand_gestures_thread = None
        self.stop_signal = threading.Event()  # 手勢停止

        # 初始化攝影機
        self.camera = QCamera(QCameraInfo.defaultCamera())
        self.cameraViewfinder = QtMultimediaWidgets.QCameraViewfinder(self.groupBox)
        self.camera.setViewfinder(self.cameraViewfinder)
        self.camera.start()  # 開啟攝影機
        self.verticalLayoutGroupBox.addWidget(self.cameraViewfinder)  

        self.timer = None  

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

        # OK 按鈕(下一步)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setFont(QtGui.QFont(self.custom_font, 18))  
        self.pushButton.setMinimumHeight(100)
        self.pushButton.setFixedWidth(400)
        self.pushButton.setText("OK")
        #self.pushButton.clicked.connect(self.close)  # 執行後關閉頁面

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

        self.pushButton.clicked.connect(self.on_next_clicked)
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.title_label.setText(_translate("MainWindow", "請玩家站定位"))

    def set_camera_viewfinder(self, camera_viewfinder):
        if not self.cameraViewfinder or not self.cameraViewfinder.isVisible():
            if self.cameraViewfinder:
                self.cameraViewfinder.setParent(None)  # 移除舊的視圖
                self.cameraViewfinder.deleteLater()

            # 新的攝影機圖框
            self.cameraViewfinder = QtMultimediaWidgets.QCameraViewfinder(self.groupBox)
            self.camera = QCamera(QCameraInfo.defaultCamera())
            self.camera.setViewfinder(self.cameraViewfinder)
            self.camera.start()
            self.verticalLayoutGroupBox.addWidget(self.cameraViewfinder)  # 添加到佈局
            self.cameraViewfinder.show()

    def init_camera(self):
        # 刪除舊的攝影機圖框
        if self.cameraViewfinder:
            self.cameraViewfinder.setParent(None)
            self.cameraViewfinder.deleteLater()

        # 新增新的攝影機圖框
        self.cameraViewfinder = QtMultimediaWidgets.QCameraViewfinder(self.groupBox)
        self.camera = QCamera(QCameraInfo.defaultCamera())
        self.camera.setViewfinder(self.cameraViewfinder)
        self.camera.start()
        
        self.verticalLayoutGroupBox.addWidget(self.cameraViewfinder)
        self.cameraViewfinder.show()

    def restart_camera(self):
        if self.cameraViewfinder:
                self.cameraViewfinder.setParent(None)  # 移除舊的攝影機視圖
                self.cameraViewfinder.deleteLater()  # 確保舊的視圖被釋放

        # 重新初始化攝影機視圖
        self.cameraViewfinder = QtMultimediaWidgets.QCameraViewfinder(self.groupBox)
        self.camera = QCamera(QCameraInfo.defaultCamera())
        self.camera.setViewfinder(self.cameraViewfinder)
        self.camera.start()
            
        # 添加攝影機視圖到界面的 verticalLayoutGroupBox
        self.verticalLayoutGroupBox.addWidget(self.cameraViewfinder)
        self.cameraViewfinder.show()

    # 上一頁的難易度
    def set_difficulty(self, difficulty):
        print(f"Setting difficulty: {difficulty}") 
        self.difficulty_label.setText(f"難易度: {difficulty}")

    # 上一步
    def on_prev_clicked(self):
        self.prevButton_clicked.emit()  

    # 下一步
    def on_next_clicked(self):
        self.pushButton_clicked.emit()
        print("Next button clicked.")  # 添加这一行来调试

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
    # def stop_hand_gestures_detection(self):
    #     if self.hand_gestures_thread is not None and self.hand_gestures_thread.is_alive():
    #         self.stop_signal.set()  
    #         self.hand_gestures_thread.join()
    #     self.cancel_timer()  # 在這裡取消計時器

    def stop_hand_gestures_detection(self):
        if self.hand_gestures_thread is not None and self.hand_gestures_thread.is_alive():
            self.stop_signal.set()  # 停止手勢偵測執行緒
            self.hand_gestures_thread.join()
        self.cancel_timer()  # 取消計時器

        # 確保攝影機持續運行
        if self.camera.state() != QCamera.ActiveState:
            self.camera.start()

    def hand_gestures_detection(self):
        for gesture in detect_hand_gestures():
            if self.stop_signal.is_set():  # 檢查要不要停止
                break
            self.handle_gesture(gesture)

    # 按鈕手勢對比
    # def handle_gesture(self, gesture):
    #     print(f"Detected gesture: {gesture}")
    #     if gesture == 'back':
    #         self.highlight_button(self.prevButton)
    #         #self.on_prev_clicked()
    #         threading.Timer(3, self.on_prev_clicked).start()
    #         self.stop_signal.set()
    #     elif gesture == 'ok':
    #         self.highlight_button(self.pushButton)
    #         threading.Timer(3, self.on_next_clicked).start()
    #         print("OK gesture detected, about to trigger next button.")  # Debug statement
    #         self.stop_signal.set()

    def handle_gesture(self, gesture):
        print(f"Detected gesture: {gesture}")
        if gesture == 'back':
            self.highlight_button(self.prevButton)
            threading.Timer(3, self.on_prev_clicked).start()
            self.stop_signal.set()
        elif gesture == 'ok':
            self.highlight_button(self.pushButton)
            threading.Timer(3, self.on_next_clicked).start()
            print("OK gesture detected, about to trigger next button.")
            self.stop_signal.set()

        # 確保攝影機保持活躍
        if self.camera.state() != QCamera.ActiveState:
            self.camera.start()

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
        self.prevButton.setStyleSheet("")  
        self.pushButton.setStyleSheet("")

    # 以防攝影機錯誤處理
    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            # 確保圖像處理
            frame = cv2.resize(frame, (1700, 900))
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(qt_image))
        else:
            print("Failed to read from camera.")

    # def closeEvent(self, event):
    #     self.stop_hand_gestures_detection()  
    #     if self.cameraViewfinder:
    #         self.cameraViewfinder.setParent(None)  

    #     # 關閉所有視窗
    #     for widget in QtWidgets.QApplication.topLevelWidgets():
    #         if widget is not self and isinstance(widget, QtWidgets.QWidget):
    #             widget.close()

    #     event.accept()  # 關閉事件

    # 關閉資訊
    def closeEvent(self, event):
        self.stop_hand_gestures_detection()  
        super().closeEvent(event)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_NewStandBy()
    MainWindow.setCentralWidget(ui)
    
    MainWindow.show()
    sys.exit(app.exec_())
