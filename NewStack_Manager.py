import cv2
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from Screen.NewSelect_Name import Ui_NewSelectName
from Screen.NewGame_Instructions import Ui_NewGameInstructions
from Screen.NewSelect_Difficulty import Ui_NewSelectDifficulty
from Screen.NewStandBy import Ui_NewStandBy

class NewStackManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setObjectName("MainWindow")
        screen = QtWidgets.QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        self.setGeometry(screen_geometry)
        self.setWindowTitle('MainWindow')

        # 攝影機
        self.camera = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.video_label = QLabel()  

        # 遊戲頁面
        self.pages = [
            Ui_NewSelectName(),
            Ui_NewGameInstructions(),
            Ui_NewSelectDifficulty(),
            Ui_NewStandBy()
        ]
        self.current_page_index = 0

        self.centralwidget = QWidget(self)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.setCentralWidget(self.centralwidget)
        self.show_page(self.current_page_index)

        self.setup_connections()

        self.start_hand_gestures_detection(self.current_page_index)

    def setup_connections(self):
        for page in self.pages:
            if hasattr(page, 'nextButton_clicked'):
                page.nextButton_clicked.connect(self.show_next_page)
            if hasattr(page, 'prevButton_clicked'):
                page.prevButton_clicked.connect(self.show_previous_page)
            if hasattr(page, 'role_selected'):
                page.role_selected.connect(self.show_next_page_with_role)
            if hasattr(page, 'difficulty_selected'):
                page.difficulty_selected.connect(self.on_difficulty_selected)

    # 開始手勢辨識判斷
    def start_hand_gestures_detection(self, index):
        page = self.pages[index]
        if hasattr(page, 'start_hand_gestures_detection'):
            page.start_hand_gestures_detection()
        print(f"Hand gestures detection started on page index: {index}")

    # 關閉手勢辨識
    def stop_current_hand_gestures_detection(self):
        page = self.pages[self.current_page_index]
        if hasattr(page, 'stop_hand_gestures_detection'):
            page.stop_hand_gestures_detection()
        print(f"Hand gestures detection stopped on page index: {self.current_page_index}")

    # 切換頁面
    def show_page(self, index):
        if self.centralwidget.layout().count() > 0:
            self.centralwidget.layout().itemAt(0).widget().setParent(None)

        page = self.pages[index]
        self.centralwidget.layout().addWidget(page)

        if isinstance(page, Ui_NewStandBy):
            if self.video_label.parent() is None:
                if hasattr(page, 'verticalLayoutGroupBox'):
                    layout = page.verticalLayoutGroupBox
                    layout.addWidget(self.video_label)
                else:
                    self.centralwidget.layout().addWidget(self.video_label)
            
            self.start_streaming()
        else:
            self.stop_streaming()

    # 下一頁
    def show_next_page(self):
        if self.current_page_index < len(self.pages) - 1:
            self.stop_current_hand_gestures_detection()
            self.current_page_index += 1
            self.show_page(self.current_page_index)
            print(f"Switched to page index: {self.current_page_index}")
            self.start_hand_gestures_detection(self.current_page_index)

    # 上一頁
    def show_previous_page(self):
        if self.current_page_index > 0:
            self.stop_current_hand_gestures_detection()
            self.current_page_index -= 1
            self.show_page(self.current_page_index)
            print(f"Switched to page index: {self.current_page_index}")
            self.start_hand_gestures_detection(self.current_page_index)
        else:
            print("已經是第一頁，不能返回。")

    # 選擇角色
    def show_next_page_with_role(self, role):
        if self.current_page_index < len(self.pages) - 1:
            self.stop_current_hand_gestures_detection()
            self.current_page_index += 1
            next_page = self.pages[self.current_page_index]

            if isinstance(next_page, Ui_NewGameInstructions):
                next_page.set_team_name(role)

            self.show_page(self.current_page_index)
            print(f"角色選擇: {role}, 切換頁面: {self.current_page_index}")
            self.start_hand_gestures_detection(self.current_page_index)

    # 選擇難易度
    def on_difficulty_selected(self, difficulty):
        print(f"難易度選擇: {difficulty}")

        if isinstance(self.pages[3], Ui_NewStandBy):
            self.pages[3].set_difficulty(difficulty)
        self.show_next_page()

    def start_streaming(self):
        self.timer.start(20)  

    def stop_streaming(self):
        self.timer.stop()
        self.video_label.clear()

    # 攝影機圖框
    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.resize(frame, (1700,900))  # 攝影機圖框尺寸

            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(qt_image))
            self.video_label.setFixedSize(1700, 900)  

    # 關閉攝影機
    def closeEvent(self, event):
        self.stop_streaming()
        self.camera.release()
        print("Camera stopped in NewStackManager.")
        super().closeEvent(event)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = NewStackManager()
    MainWindow.show()
    sys.exit(app.exec_())
