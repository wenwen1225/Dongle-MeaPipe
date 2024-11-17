import random
import os
import sys
import threading
import mysql.connector as db
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QGridLayout, QWidget, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QTimer

from KL_MP_Mix import detect_hand_gestures

# 正確.錯誤.跳過 頁面
from Screen.Correct import Ui_Correct  # 正確
from Screen.Error import Ui_Error  # 錯誤1
from Screen.Pass import Ui_Pass  # 跳過
from Screen.vid import Ui_Error2  # 錯誤2
from Screen.test import Ui_Error3  # 錯誤3

class Ui_Game_Start(QtWidgets.QWidget):
    delay = 30  # 文字動畫延遲
    question_number = 1  # 題號
    countdown_seconds = 360  # 倒數初始秒數
    question_updated = False
    max_space_count = 3  # 空白鍵跳題限制次數
    pass_count = 0  # 跳過次數
    total_score = 0  # 總分
    error_count = 0  # 錯誤次數 

    def __init__(self, parent=None):
        super().__init__(parent)  # 將父物件傳入
        self.setParent(parent)  # 設置父物件
        self.animation_finished = False
        self.animation_in_progress = True
        self.question_updated = False
        self.total_score = 0

        # 初始化時讀取難度並根據難度設定 score
        self.team_name, self.difficulty = self.read_save_file()  # 調用 read_save_file() 函數取得難度
        self.score = self.get_score_for_difficulty(self.difficulty)

        # 設置主佈局
        self.layout = QVBoxLayout()
        self.setLayout(self.layout) 

        # 設定視窗
        self.setWindowTitle("MainWindow")
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        # 背景圖片
        self.label = QLabel(self)
        self.background = QPixmap("Font/game.jpg")
        self.update_background()
        self.label.setGeometry(0, 0, self.width(), self.height())

        # 加載字體
        font_path = os.path.join(os.path.dirname(__file__), "Font", "NaikaiFont-Bold.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(family, 20)
        self.letter_spacing = 150
        font.setLetterSpacing(QFont.PercentageSpacing, self.letter_spacing)

        # 創建頂部橫向布局
        top_layout = QHBoxLayout()

        # 題號顯示區域
        self.question_label = QLabel(f"第{self.question_number}題", self)
        self.question_label.setFont(font)
        self.question_label.setStyleSheet("background-color: transparent; color: black;")
        
        # 倒數時間顯示區域
        self.timer_label = QLabel(f"倒數時間: {self.countdown_seconds} 秒", self)
        self.timer_label.setFont(font)
        self.timer_label.setStyleSheet("background-color: transparent; color: black;")
        
        # 添加題號和倒數時間到頂部橫向佈局
        top_layout.addWidget(self.question_label, alignment=Qt.AlignLeft)
        top_layout.addStretch()  # 用於分隔題號和倒數時間
        top_layout.addWidget(self.timer_label, alignment=Qt.AlignRight)
        
        # 將頂部橫向佈局添加到主佈局頂部
        self.layout.addLayout(top_layout)

        # 設定倒數計時器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # 每秒觸發一次

        # 文字顯示區域
        self.text_label = QLabel(self)
        self.text_label.setFont(font)
        self.text_label.setStyleSheet("background-color: transparent; color: black;")
        self.text_label.setAlignment(Qt.AlignCenter)
        
        # 將文字顯示區域添加到主佈局
        self.layout.addWidget(self.text_label, alignment=Qt.AlignTop | Qt.AlignCenter)

        # 選項和圖示布局容器
        self.option_widget = QWidget(self)
        self.option_layout = QGridLayout(self.option_widget)
        self.option_widget.setVisible(False)
        
        # 將選項容器添加到主佈局
        self.layout.addWidget(self.option_widget, alignment=Qt.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 200)
        self.layout.setSpacing(0)

    # 讀取設定檔進行資料庫連線
    def get_config(self):
        config = {}
        config_path = os.path.join(os.path.dirname(__file__), 'Data', 'config.txt')
        with open(config_path, 'r') as f:
            for line in f:
                key, value = line.strip().split('=')
                config[key.strip()] = value.strip()
        return config
    
    # 連接資料庫
    def display_random_topic(self, difficulty):
        try:
            config = self.get_config()
            connection = db.connect(
                host=config['host'],
                user=config['user'],
                password=config.get('password', ''),
                database=config['database']
            )
            cursor = connection.cursor()

            # 根據難易度選擇分數
            if self.difficulty =="隨機挑戰":
                random_score = random.choice([2, 4, 6])
                cursor.execute("SELECT 題目, 錯字, 錯字位置 FROM topic WHERE 分數 = %s;", (random_score,))
            else:
                cursor.execute("SELECT 題目, 錯字, 錯字位置 FROM topic WHERE 分數 = %s;", (self.score,))
            
            rows = cursor.fetchall()
            if rows:
                topic, typo, typo_position= random.choice(rows)
                typo = typo[:5] if len(typo) > 5 else typo
                return topic or "", typo, typo_position or ""
            return "", "", ""
        except db.Error as e:
            print("資料庫錯誤:", e)
            return "", "", ""
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    # 讀取 save.txt
    def read_save_file(self):
        try:
            with open("Data/save.txt", "r", encoding="big5") as file:  # 修改編碼為 big5 或 gbk
                lines = file.readlines()
                global team_name
                global difficulty
                self.team_name = lines[0].strip()
                self.difficulty = lines[1].strip()
                print(f"隊名: {self.team_name}, 難易度: {self.difficulty}")  # 打印隊名和難易度
                return self.team_name, self.difficulty
        except FileNotFoundError:
            print("save.txt not found.")
            return None, None
        except UnicodeDecodeError as e:
            print(f"Encoding error: {e}")
            return None, None   
     
    # 區分難易度
    def get_score_for_difficulty(self, difficulty):
        if difficulty == "簡單":
            print("簡單")
            return 2
        elif difficulty == "普通":
            print("普通")
            return 4
        elif difficulty == "困難":
            print("困難")
            return 6
        else:
            print(f"未知難易度: {difficulty}")
            return None # 當難易度無效時返回 None

    # 倒數時間判斷
    def update_timer(self):
        self.countdown_seconds -= 1
        self.timer_label.setText(f"時間: {self.countdown_seconds} 秒")

        # 檢查倒數時間是否為零
        if self.countdown_seconds <= 0:
            self.close_all_windows()

    # 關閉所有視窗
    def close_all_windows(self):
        QtWidgets.QApplication.instance().quit()

    # 鍵盤事件
    def keyPressEvent(self, event):
        if self.animation_in_progress:
            print("Animation in progress. Key press ignored.")
            return

        # 處理不同按鍵
        if event.key() == Qt.Key_Space:  # 空白鍵跳題
            if self.pass_count < self.max_space_count:
                self.pass_count += 1
                self.question_number += 1  # 題號增加
                self.clear_page()
                self.show_next_question()
                self.parent().show_pass_popup()
            else:
                self.close_all_windows()  # 超過次數，結束遊戲
        elif event.key() == Qt.Key_Escape:  # Esc 顯示下一題
            self.question_number += 1
            self.clear_page()
            self.show_next_question()
        elif event.key() == Qt.Key_Q:  # Q 結束遊戲
            self.close_all_windows()

    # 更新題號
    def update_question_number(self):
        self.question_number += 1
        self.question_label.setText(f"第{self.question_number}題")
        self.clear_page()  # 清除頁面
        self.show_next_question()  # 顯示下一題
        self.animation_in_progress = True  # 新一題動畫開始
        self.question_updated = True

    # 調整視窗、文字、圖片大小
    def resizeEvent(self, event):
        base_font_size = self.width() // 50 
        font = self.text_label.font()
        font.setPointSize(base_font_size)
        self.text_label.setFont(font)
        self.question_label.setFont(font)
        self.timer_label.setFont(font)

        # 縮放背景圖
        scaled_background = self.background.scaled(self.width(), self.height(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.label.setPixmap(scaled_background)
        self.label.setGeometry(0, 0, self.width(), self.height())

        # 動態調整選項的字體大小
        for i in range(self.option_layout.count()):
            widget = self.option_layout.itemAt(i).widget()
            if isinstance(widget, QLabel) and widget.text():  # 檢查是否為文字的 QLabel
                widget.setFont(font)  # 設置與題目相同的字體大小

        # 動態調整圖示大小
        icon_size = min(self.width(), self.height()) // 50  # 調整圖示大小比例因子
        for i in range(self.option_layout.count()):
            widget = self.option_layout.itemAt(i).widget()
            if isinstance(widget, QLabel) and widget.pixmap():  # 檢查是否為圖示的 QLabel
                scaled_icon = widget.pixmap().scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                widget.setPixmap(scaled_icon)

        super().resizeEvent(event)

    # 縮放背景圖
    def update_background(self):
        # 按照視窗大小縮放背景圖並設置
        scaled_background = self.background.scaled(self.width(), self.height(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.label.setPixmap(scaled_background)
        self.label.setGeometry(0, 0, self.width(), self.height())

    # 清除頁面中的所有文字和選項
    def clear_page(self):
        self.text_label.clear()
        self.option_widget.setVisible(False)  # 隱藏選項和圖示
        self.question_label.setText(f"第{self.question_number}題")  # 確保題號更新
        for i in reversed(range(self.option_layout.count())):
            widget = self.option_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # 刪除現有的選項和圖示

        # 調整字體大小
        font = self.text_label.font()
        base_size = self.width() // 50  
        font.setPointSize(base_size)
        self.text_label.setFont(font)

    # 顯示成語題目
    def show_question_and_options(self, difficulty): 
        while True:
            # 在隨機挑戰模式下，每次都生成新的隨機難易度分數
            if self.difficulty == "隨機挑戰":
                self.score = random.choice([2, 4, 6])  # 設置隨機分數為 self.score
                topic, typo, typo_position = self.display_random_topic(self.score)
                print(f"題目分數: {self.score}")
            else:
                topic, typo, typo_position = self.display_random_topic(self.score)

            # 顯示題目選項
            if not topic or not typo or not typo_position:
                print("跳過不完整的題目...")
                continue

            result = self.generate_unique_options(typo, typo_position)
            if result is None:
                print("跳過無效選項...")
                continue

            replacement_char, options = result

            # 將替換字插入到題目中
            topic_with_typo = list(topic)
            try:
                topic_with_typo[int(typo_position)] = replacement_char
            except (IndexError, ValueError):
                print("跳過無效替換...")
                continue

            # 顯示題目與選項
            highlighted_text = ''.join(topic_with_typo)
            self.text_label.setTextFormat(Qt.RichText)
            self.show_text_with_random_effect(highlighted_text, typo, options)

            # 顯示選項與圖標
            self.display_options_and_icons(options)
            break

    # 錯字排除，隨機選取一個錯字，排除第一個字元
    def get_random_typo(self, typo):
        # correct_answer = typo[0]
        typo_options = list(typo[1:])  # 排除第一個字元
        return random.choice(typo_options)

    # 錯字選項
    def generate_unique_options(self, typo, typo_position):
        try:
            typo_position = int(typo_position)
        except ValueError:
            print("錯誤：無效的 typo_position 值，無法轉換為整數")
            return None  # 當無法轉換時，直接返回 None，這樣可以跳過這一題

        # 確保 typo_position 在 typo 範圍內
        if typo_position < 0 or typo_position >= len(typo):
            print(f"錯誤：錯字位置 '{typo_position}' 無效，應在 0 到 {len(typo)-1} 之間")
            return None  # 如果位置錯誤，返回 None，繼續下一題

        try:
            self.correct_answer = typo[0]
            typo_options = list(typo[1:])
            
            # 確保有足夠的錯誤選項
            if len(typo_options) < 3:
                print(f"警告：錯誤選項數量不足，跳過此題")
                return None  # 如果選項不足，跳過這一題

            replacement_char = random.choice(typo_options)

            # 為題目中的錯字加上紅色標記
            highlighted_replacement_char = f"<span style='color:red'>{replacement_char}</span>"
            
            # 生成錯字選項
            unique_options = [self.correct_answer]
            typo_options = [char for char in typo_options if char != replacement_char]
            
            # 隨機選擇 3 個錯誤選項並打亂
            unique_options.extend(random.sample(typo_options, 3))
            random.shuffle(unique_options)

            return highlighted_replacement_char, unique_options
        
        except Exception as e:
            print(f"錯誤：生成選項時發生錯誤，錯誤訊息：{e}")
            return None  # 若有任何錯誤，返回 None，繼續下一題

    # 選項擺放
    def display_options_and_icons(self, options):
        # 清空現有布局中的內容
        for i in reversed(range(self.option_layout.count())):
            widget = self.option_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # 安排並樣式化選項和圖示
        for i, option in enumerate(options):
            button = QPushButton(option, self)  # 使用 QPushButton 替換 QLabel
            button.setFont(self.text_label.font())
            
            # 按鈕樣式
            button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: black;
                    border: none;
                    text-align: center;
                }
            """)
            
            button.setFixedSize(200, 200)  # 設定按鈕大小
            button.setFocusPolicy(Qt.StrongFocus)
            
            # 當按鈕被點擊時，修改字體顏色為紅色
            button.clicked.connect(lambda _, btn=button: self.check_answer(btn))  # 綁定選項文字至 check_answer

            row, col = divmod(i, 2)  # 計算行列位置
            self.option_layout.addWidget(button, row * 2, col)  # 每行放2個選項

        # 顯示圖示，並按照順序放置
        icon_paths = [f'Pic/icon{i}.png' for i in range(1, 5)]
        icons = [QPixmap(icon).scaled(150, 150, Qt.KeepAspectRatio) for icon in icon_paths if os.path.exists(icon)]
        
        # 確保圖示有4個，並將它們安排到對應位置
        icon_positions = [(0, 0), (0, 1), (1, 0), (1, 1)]  # (行, 列) => (0,0)放圖示1，(0,1)放圖示2，依此類推
        for pixmap, (row, col) in zip(icons, icon_positions):
            icon_label = QLabel(self)
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(Qt.AlignCenter)
            self.option_layout.addWidget(icon_label, row * 2 + 1, col)  # 圖示放在選項下面，所以下一行

    # 圖示擺放
    def show_icons(self):
        icon_paths = [f'Pic/icon{i}.png' for i in range(1, 5)]
        icons = [QPixmap(icon).scaled(100, 100, Qt.KeepAspectRatio) for icon in icon_paths if os.path.exists(icon)]
        icon_positions = [(270, 350), (270, 450), (430, 350), (430, 450)]

        for pixmap, (x, y) in zip(icons, icon_positions):
            icon_label = QLabel(self)
            icon_label.setPixmap(pixmap)
            icon_label.setGeometry(x, y, 100, 100)
            self.option_layout.addWidget(icon_label)

    # 按鈕字持紅色字體
    def check_answer(self, selected_option):
        selected_option.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: red;
            }
        """)

        QTimer.singleShot(500, lambda: self.compare_answer(selected_option))

    # 比對選擇的答案是否為正確答案
    def compare_answer(self, selected_option):
        if selected_option.text() == self.correct_answer:
            print("答對了!")
             # 防禦性檢查，確保 self.score 是數字
            if self.score is not None and isinstance(self.score, (int, float)):
                self.total_score += self.score  # 加上當前題目的分數
            else:
                print("警告：分數未定義或類型不正確，無法加分")
            print(f"分數: {self.total_score}")
            self.parent().show_correct_popup()
        else:
            self.error_count += 1
            print(f"答錯了! 錯誤次數: {self.error_count}")

            # 根據錯誤次數顯示對應的彈窗
            if self.error_count == 1:
                self.parent().show_error_popup()
                print(f"分數: {self.total_score}")
            elif self.error_count == 2:
                self.parent().show_error2_popup()
                print(f"分數: {self.total_score}")
            elif self.error_count == 3:
                self.parent().show_error3_popup()
                print("遊戲結束，3次答錯後關閉遊戲")
                QTimer.singleShot(3000, self.close_all_windows)  # 延遲 3 秒後關閉遊戲
                return  # 結束處理，避免進一步執行

        QTimer.singleShot(2200, self.show_next_question)  # 延遲 2 秒後跳至下一題
        self.update_question_number()

    # 顯示下一題
    def show_next_question(self):
        self.clear_page()
        self.show_question_and_options(self.difficulty)
        self.question_label.setText(f"第{self.question_number}題")
        self.animation_finished = True
        self.animation_in_progress = True
        self.question_updated = False
        
    def on_animation_finished(self):
        self.animation_finished = False  # 動畫結束

    # 文字特效方法
    def show_text_with_random_effect(self, text1, typo, options):
        # 初始化動畫狀態
        self.animation_in_progress = True
        self.animation_finished = False

        # 設置字體間距
        font = self.text_label.font()
        font.setLetterSpacing(QFont.PercentageSpacing, 200)
        self.text_label.setFont(font)

        # 隨機選擇特效
        effects = [self.make_text_typewriter_effect,
                self.make_text_fade_in_effect, self.make_text_slide_in_effect]
        selected_effect = random.choice(effects)

        # 顯示所選特效的訊息
        effect_name = {
            self.make_text_typewriter_effect: "使用的是打字機效果 (Typewriter Effect)",
            self.make_text_fade_in_effect: "使用的是淡入效果 (Fade-in Effect)",
            self.make_text_slide_in_effect: "使用的是滑動進入效果 (Slide-in Effect)"
        }
        print(effect_name[selected_effect])

        # 執行選中的特效，並在動畫完成後更新 `self.animation_finished`
        selected_effect(text1, typo, lambda: self.on_effect_finished(options))

    def on_effect_finished(self, options):
        self.animation_in_progress = False  # 動畫結束，允許鍵盤事件
        self.animation_finished = True  # 動畫完成
        self.option_widget.setVisible(True)
        self.display_options_and_icons(options)

    # 文字特效1-打字機
    def make_text_typewriter_effect(self, text1, text2, on_finished):
        full_text, current_text, step = f"{text1}", "", 0

        def update_text():
            nonlocal step, current_text
            if step < len(full_text):
                current_text += full_text[step]
                self.text_label.setText(current_text)
                step += 1
            else:
                timer.stop()
                on_finished()

        timer = QTimer(self)
        timer.timeout.connect(update_text)
        timer.start(self.delay)

    # 文字特效3 - 淡入
    def make_text_fade_in_effect(self, text1, text2, on_finished):
        self.text_label.clear()
        full_text, current_opacity = f"{text1}", 0.0

        def update_opacity():
            nonlocal current_opacity
            if current_opacity <= 1.0:
                # 使用 RGBA 值調整透明度
                self.text_label.setStyleSheet(f"color: rgba(0, 0, 0, {int(current_opacity * 255)});")
                self.text_label.setText(full_text)
                current_opacity += 0.1  # 逐漸增加透明度
            else:
                timer.stop()
                on_finished()  # 動畫結束後調用回調函數

        timer = QTimer(self)
        timer.timeout.connect(update_opacity)
        timer.start(self.delay)  # 根據延遲時間設置淡入速度

    # 文字特效4 - 滑入
    def make_text_slide_in_effect(self, text1, text2, on_finished):
        # 先設置文字，確保可以測量其大小
        self.text_label.setText(text1)
        
        # 在設置文字後調整其大小以獲取準確的寬度
        self.text_label.adjustSize()
        
        # 設置起始和結束位置
        start_x = self.width()  # 起始位置設置在視窗右邊外部
        end_x = (self.width() - self.text_label.width()) // 2  # 終止位置設置為中央
        current_x = start_x

        # 定義滑入的動畫效果
        def update_position():
            nonlocal current_x
            if current_x > end_x:
                # 讓文字逐漸向左移動，當接近目標時步伐變小
                move_distance = min(20, current_x - end_x)  # 控制每次移動距離
                current_x -= move_distance
                self.text_label.move(current_x, self.text_label.y())
            else:
                # 動畫完成，確保文字停留在中央位置
                self.text_label.move(end_x, self.text_label.y())
                timer.stop()
                on_finished()  # 動畫結束後調用回調函數

        timer = QTimer(self)
        timer.timeout.connect(update_position)
        timer.start(20)  # 設置滑動效果的速度

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    game_start = Ui_Game_Start()
    game_start.show()
    game_start.show_question_and_options()  # 顯示題目和選項
    sys.exit(app.exec_())