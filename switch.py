import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

# 遊戲頁面
from Game_Start2 import Ui_Game_Start  # 遊戲畫面
from Screen.Correct import Ui_Correct  # 正確
from Screen.Error import Ui_Error  # 錯誤1
from Screen.Pass import Ui_Pass  # 跳過
from Screen.vid import Ui_Error2  # 錯誤2
from Screen.test import Ui_Error3  # 錯誤3

class GameLauncher(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MainWindow")

        # 初始化遊戲頁面
        self.game_start_window = Ui_Game_Start()
        print("已切換到Game_Start2")

        # 設定為中心窗口小部件
        self.setCentralWidget(self.game_start_window)

         # 讀取 save.txt 的內容來取得難易度
        team_name, difficulty = self.read_save_file()  # 使用讀取檔案方法取得隊名和難易度

        # 檢查是否成功取得 difficulty
        if difficulty:
            # 顯示遊戲問題和選項
            self.game_start_window.show_question_and_options(difficulty)  # 顯示問題
        else:
            print("無法顯示問題：未能讀取難易度。")

        # 顯示遊戲問題和選項
        # self.game_start_window.show_question_and_options(difficulty)  # 顯示問題

        # 設定視窗大小
        self.resize_window()
        self.show()

    # 讀取 save.txt
    def read_save_file(self):
        try:
            with open("Data/save.txt", "r", encoding="big5") as file:  # 修改編碼為 big5 或 gbk
                lines = file.readlines()
                self.team_name = lines[0].strip()
                self.difficulty = lines[1].strip()
                print(f"隊名: {self.team_name}, 難易度: {self.difficulty}")  # 打印隊名和難易度
                return self.team_name, self.difficulty
        except FileNotFoundError:
            print("save.txt not found.")
            return None, None
        except UnicodeDecodeError as e:
            print(f"Encoding error: ")

    def resize_window(self):
        screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()
        self.resize(screen_geometry.width(), screen_geometry.height())

    # 顯示答對彈窗
    def show_correct_popup(self):
        self.correct_popup = Ui_Correct()
        self.correct_popup.setupUi()
        self.correct_popup.show()
        QTimer.singleShot(2000, self.correct_popup.close)  # 2秒自動關閉

    # 顯示答錯1彈窗
    def show_error_popup(self):
        self.error_popup = Ui_Error()
        self.error_popup.setupUi()  
        self.error_popup.show()
        QTimer.singleShot(2000, self.error_popup.close)  # 2秒自動關閉

    # 顯示跳過談窗
    def show_pass_popup(self):
        self.pass_popup = Ui_Pass()
        self.pass_popup.setupUi()  
        self.pass_popup.show()
        QTimer.singleShot(2000, self.pass_popup.close)  # 2秒自動關閉
    
    # 顯示答錯2彈窗
    def show_error2_popup(self):
        self.error2_popup = Ui_Error2()
        self.error2_popup.setupUi()  
        self.error2_popup.show()
        QTimer.singleShot(2000, self.error2_popup.close)  # 2秒自動關閉

    # 顯示答錯3彈窗
    def show_error3_popup(self):
        self.error3_popup = Ui_Error3()
        self.error3_popup.setupUi()  
        self.error3_popup.show()
        QTimer.singleShot(2000, self.error3_popup.close)  # 2秒自動關閉
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    launcher = GameLauncher()
    sys.exit(app.exec_())
