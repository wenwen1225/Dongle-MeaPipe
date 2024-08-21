from PyQt5 import QtWidgets, QtMultimedia
from PyQt5.QtWidgets import QMainWindow, QWidget
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

        # 初始化頁面
        self.pages = [
            Ui_NewSelectName(),
            Ui_NewGameInstructions(),
            Ui_NewSelectDifficulty(),
            Ui_NewStandBy()
        ]
        self.current_page_index = 0

        self.centralwidget = QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.setCentralWidget(self.centralwidget)
        self.show_page(self.current_page_index)

        self.setup_connections() # 頁面連接

        # 啟動相機
        self.camera = QtMultimedia.QCamera()
        self.camera.start()
        print("Camera started in NewStackManager.")

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

    # 手勢開始
    def start_hand_gestures_detection(self, index):
        page = self.pages[index]
        if hasattr(page, 'start_hand_gestures_detection'):
            page.start_hand_gestures_detection()
        print(f"Hand gestures detection started on page index: {index}")

    # 手勢結束
    def stop_current_hand_gestures_detection(self):
        page = self.pages[self.current_page_index]
        if hasattr(page, 'stop_hand_gestures_detection'):
            page.stop_hand_gestures_detection()
        print(f"Hand gestures detection stopped on page index: {self.current_page_index}")

    def show_page(self, index):
        # Replace current page with new page
        if self.centralwidget.layout().count() > 0:
            self.centralwidget.layout().itemAt(0).widget().setParent(None)
        self.centralwidget.layout().addWidget(self.pages[index])

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
            print("Already at the first page, can't go back.")

    # 選擇角色的切換頁
    def show_next_page_with_role(self, role):
        if self.current_page_index < len(self.pages) - 1:
            self.stop_current_hand_gestures_detection()
            self.current_page_index += 1
            next_page = self.pages[self.current_page_index]
            
            if isinstance(next_page, Ui_NewGameInstructions):
                next_page.set_team_name(role)

            self.show_page(self.current_page_index)
            print(f"Role selected: {role}, switched to page index: {self.current_page_index}")
            self.start_hand_gestures_detection(self.current_page_index)

    # 選擇難易度的切換頁
    def on_difficulty_selected(self, difficulty):
        self.selected_difficulty = difficulty
        self.show_next_page()

        # 如果当前页面是 Ui_NewStandBy
        if isinstance(self.pages[self.current_page_index], Ui_NewStandBy):
            self.pages[self.current_page_index].set_difficulty(difficulty)
        
        print(f"Difficulty selected: {difficulty}")


    # 關閉攝影機
    def closeEvent(self, event):
        if self.camera:
            self.camera.stop()
            print("Camera stopped in NewStackManager.")
        super().closeEvent(event)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = NewStackManager()
    MainWindow.show()
    sys.exit(app.exec_())
