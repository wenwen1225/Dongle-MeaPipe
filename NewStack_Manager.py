import sys
from PyQt5 import QtWidgets
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

        self.pages = [Ui_NewSelectName(), Ui_NewGameInstructions(), Ui_NewSelectDifficulty(), Ui_NewStandBy()]
        self.current_page_index = 0
        self.current_camera = None

        self.centralwidget = QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.addWidget(self.pages[self.current_page_index])

        self.setCentralWidget(self.centralwidget)
        self.setup_connections()
        self.start_camera_if_needed(self.current_page_index)

    def setup_connections(self):
        for page in self.pages:
            if isinstance(page, Ui_NewGameInstructions) or isinstance(page, Ui_NewSelectDifficulty) or isinstance(page, Ui_NewStandBy):
                if hasattr(page, 'nextButton_clicked'):
                    page.nextButton_clicked.connect(self.show_next_page)
                if hasattr(page, 'prevButton_clicked'):
                    page.prevButton_clicked.connect(self.show_previous_page)
            if isinstance(page, Ui_NewSelectDifficulty):
                page.difficulty_selected.connect(self.on_difficulty_selected)
            if isinstance(page, Ui_NewSelectName):
                page.role_selected.connect(self.show_next_page_with_role)

    def start_camera_if_needed(self, index):
        # 確保每個頁面都啟動攝影機
        page = self.pages[index]
        if hasattr(page, 'camera'):
            self.current_camera = page.camera
            if self.current_camera:
                self.current_camera.start()
                print(f"Camera started on page index: {index}")
        else:
            print(f"No camera found on page index: {index}")

    def stop_current_camera(self):
        # 停止當前頁面的攝影機
        if self.current_camera:
            self.current_camera.stop()
            print(f"Camera stopped on page index: {self.current_page_index}")
            self.current_camera = None

    # 下一步
    def show_next_page(self):
        if self.current_page_index < len(self.pages) - 1:
            self.stop_current_camera()
            self.current_page_index += 1
            self.centralwidget.layout().itemAt(0).widget().setParent(None)
            self.centralwidget.layout().insertWidget(0, self.pages[self.current_page_index])
            print(f"Switched to page index: {self.current_page_index}") 
            self.start_camera_if_needed(self.current_page_index)

    # 上一步
    def show_previous_page(self):
        if self.current_page_index > 0:
            self.stop_current_camera()
            self.current_page_index -= 1
            self.centralwidget.layout().itemAt(0).widget().setParent(None)
            self.centralwidget.layout().insertWidget(0, self.pages[self.current_page_index])
            print(f"Switched to page index: {self.current_page_index}")  
            self.start_camera_if_needed(self.current_page_index)
        else:
            print("Already at the first page, can't go back.")
    
    # 選擇名稱
    def show_next_page_with_role(self, role):
        if self.current_page_index < len(self.pages) - 1:
            if isinstance(self.pages[self.current_page_index + 1], Ui_NewGameInstructions):
                self.stop_current_camera()
                self.current_page_index += 1
                self.centralwidget.layout().itemAt(0).widget().setParent(None)
                self.pages[self.current_page_index].set_team_name(role)
                self.centralwidget.layout().insertWidget(0, self.pages[self.current_page_index])
                print(f"Role selected: {role}, switched to page index: {self.current_page_index}")
                self.start_camera_if_needed(self.current_page_index)

    # 選擇困難度
    def on_difficulty_selected(self, difficulty):
        self.selected_difficulty = difficulty
        self.show_next_page()
        print(f"Difficulty selected: {difficulty}")  

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = NewStackManager()
    MainWindow.show()
    sys.exit(app.exec_())
