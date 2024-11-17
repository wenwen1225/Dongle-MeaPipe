import cv2
import os
from PyQt5 import QtWidgets, QtMultimedia
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, QUrl

# 各頁面
from Screen.NewSelect_Name import Ui_NewSelectName
from Screen.NewGame_Instructions import Ui_NewGameInstructions
from Screen.NewSelect_Difficulty import Ui_NewSelectDifficulty
from Screen.NewStandBy import Ui_NewStandBy
from Screen.Ready import Ui_Ready
from switch import GameLauncher
# from Game_Start import Ui_Game_Start

class NewStackManager(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化背景音樂播放器
        # self.background_music = QtMultimedia.QMediaPlayer()
        # music_path = os.path.join(os.path.dirname(__file__), "Font", "music.mp3")
        # self.background_music.setMedia(QtMultimedia.QMediaContent(QUrl.fromLocalFile(music_path)))
        # self.background_music.setVolume(30)  # 設定音量，可以根據需求調整
        # self.background_music.play()  # 播放背景音樂

        # # 設定音樂循環播放
        # self.background_music.mediaStatusChanged.connect(self.handle_media_status_change)

        self.setObjectName("MainWindow")
        screen = QtWidgets.QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        self.setGeometry(screen_geometry)
        self.setWindowTitle('MainWindow')

        # Set light blue background for the entire window except buttons
        self.setStyleSheet("""
            QWidget {
                background-color: #dffaff;  /* Light blue background for all widgets */
            }
            QPushButton {
                background-color: white;  /* White background for buttons */
            }
        """)

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
            Ui_NewStandBy(),
            Ui_Ready(),
            # Ui_Game_Start()
        ]
        self.current_page_index = 0

        self.centralwidget = QWidget(self)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.setCentralWidget(self.centralwidget)
        self.verticalLayout.addWidget(self.video_label)

        self.show_page(self.current_page_index)
        self.setup_connections()
        self.start_hand_gestures_detection(self.current_page_index)

        # 連接Ui_Ready的播放完成信號到切換方法
        ready_page = self.pages[-1]
        if isinstance(ready_page, Ui_Ready):
            ready_page.video_finished.connect(self.on_ready_finished)

    def on_ready_finished(self):
        # 停止並釋放頁面資源
        # self.stop_current_hand_gestures_detection()
        self.close_all_pages()
        self.close()

        # 啟動switch中的GameLauncher以顯示遊戲頁面
        self.launch_game()

    def close_all_pages(self):
        # 釋放所有頁面資源
        for page in self.pages:
            if isinstance(page, QWidget):
                page.deleteLater()
        self.camera.release()
        print("所有頁面已釋放資源")

    def launch_game(self):
        # 開啟GameLauncher顯示遊戲主體
        self.game_launcher = GameLauncher()  # 創建GameLauncher實例
        self.game_launcher.show()
        print("已切換到Game_Start2")

    # def handle_media_status_change(self, status):
    #     if status == QtMultimedia.QMediaPlayer.EndOfMedia:
    #         self.background_music.setPosition(0)  # 回到音樂開頭
    #         self.background_music.play()  # 重新播放

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # 視窗大小
        width = self.width()
        height = self.height()

        # 攝影機圖框大小
        self.video_label.setFixedSize(int(width * 0.8), int(height * 0.6))  

    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            # 視窗大小
            width = self.video_label.width()
            height = self.video_label.height()
            
            # 調整攝影機大小
            frame = cv2.resize(frame, (width, height))

            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    # 按鈕的切換頁
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
            if hasattr(page, 'pushButton_clicked'):
                page.pushButton_clicked.connect(self.show_next_page)
            # if isinstance(page, Ui_Ready):
            #     page.video_finished.connect(self.go_to_game_start)   

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

        # 重新初始化攝影機圖框
        if isinstance(page, Ui_NewStandBy):
            page.restart_camera()
        # elif isinstance(page, Ui_Game_Start):
        #     page.showTextDrop("Font\\NaikaiFont-Bold.ttf", "Font\\game.jpg")
        #     self.start_streaming()  # 啟動攝影機
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
        self.selected_role = role  # 儲存角色選擇
        self.save_to_file(self.selected_role, getattr(self, 'selected_difficulty', ''))
        
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
        self.selected_difficulty = difficulty  # 儲存難易度選擇
        self.save_to_file(getattr(self, 'selected_role', ''), self.selected_difficulty)

        if isinstance(self.pages[3], Ui_NewStandBy):
            self.pages[3].set_difficulty(difficulty)
        self.show_next_page()

    # 寫入save.txt檔
    def save_to_file(self, role, difficulty):
        file_path = os.path.join(os.path.dirname(__file__), "Data", "save.txt")
        with open(file_path, 'w') as file:
            file.write(f"{role}\n")
            file.write(f"{difficulty}\n")
        print(f"Saved role: {role}, difficulty: {difficulty} to {file_path}")

    # 遊戲頁面切換
    # def go_to_game_start(self):
    #     self.current_page_index = len(self.pages) - 1  
    #     self.show_page(self.current_page_index)
    #     print("影片播放完畢，切換到遊戲開始頁面")

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
            print(f"Frame read successfully: {ret}")

    # 關閉攝影機
    # def closeEvent(self, event):
    #     self.stop_streaming()
    #     self.camera.release()
    #     print("Camera stopped in NewStackManager.")
    #     super().closeEvent(event)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = NewStackManager()
    MainWindow.show()
    sys.exit(app.exec_())
