import random
import cv2
import numpy as np
import mysql.connector as db
import os
import time
from PyQt5 import QtCore, QtWidgets, QtGui
from PIL import ImageFont, ImageDraw, Image
from KL_MP_Mix import detect_hand_gestures

class Ui_Game_Start(QtWidgets.QWidget):
    letter_spacing = 40

    def __init__(self):
        super().__init__()

        # 創建 QLabel
        self.video_label = QtWidgets.QLabel(self)
        self.video_label.setScaledContents(True)  # 啟用縮放內容
        
        # 設定佈局，確保 QLabel 可以根據父容器的大小變化
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.video_label)
        self.setLayout(layout)

    def resizeEvent(self, event):
        # 獲取新的大小
        new_size = event.size()
        self.video_label.resize(new_size)  # 調整 QLabel 大小
        super().resizeEvent(event)  # 確保父類別的 resizeEvent 被調用

    def Get_Config():
        config = {}
        base_dir = os.path.dirname(__file__)  
        config_path = os.path.join(base_dir, 'Data', 'config.txt')
        
        with open(config_path, 'r') as f:
            for line in f:
                key, value = line.strip().split('=')
                config[key.strip()] = value.strip()
        
        return config

    # 連接資料庫
    def Display_Random_Topic():
        try:
            config = Ui_Game_Start.Get_Config()
            connect = db.connect(
                host=config['host'],
                user=config['user'],
                password=config.get('password', ''),
                database=config['database']
            )
            cursor = connect.cursor()
            query = "SELECT 題目, 錯字, 錯字位置 FROM topic;"
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows:
                # 隨機選擇一行
                random_row = random.choice(rows)
                topic = random_row[0] or ""  # SQL資料表中題目那一欄
                typo = random_row[1] or ""   # SQL資料表中錯字那一欄
                typo_position = str(random_row[2] or "")

                # 確保錯字不超過四個
                if len(typo) > 5:
                    typo = typo[:4]  # 限制錯字長度

                return topic, typo, typo_position   # 返回 '題目'、'錯字' 和 '錯字位置'
            else:
                print("没有找到任何題目")
                return "", "", ""
        except db.Error as error:
            print("資料庫查詢錯誤:", error)
            return "", "", ""
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connect' in locals():
                connect.close()

    # 文字特效1
    def makeTextTypewriterEffect(img, text1, text2, positions, font_path, delay):
        """顯示打字機效果的文字，並增加字間距。"""
        font_size = 38
        font = ImageFont.truetype(font_path, font_size)

        steps = max(len(text1), len(text2))

        for step in range(steps + 1):
            img_pil = Image.fromarray(img.copy())
            draw = ImageDraw.Draw(img_pil)

            # 第一行文字
            if step <= len(text1):
                current_x1 = (img.shape[1] - (len(text1[:step]) * (font_size + Ui_Game_Start.letter_spacing))) // 2
                for i, char in enumerate(text1[:step]):
                    draw.text((current_x1 + i * (font_size + Ui_Game_Start.letter_spacing), positions[0][1]), char, font=font, fill=(0, 0, 0))

            # 第二行文字
            if step <= len(text2):
                current_x2 = (img.shape[1] - (len(text2[:step]) * (font_size + Ui_Game_Start.letter_spacing))) // 2
                for i, char in enumerate(text2[:step]):
                    draw.text((current_x2 + i * (font_size + Ui_Game_Start.letter_spacing), positions[1][1]), char, font=font, fill=(0, 0, 0))

            img_copy = np.array(img_pil)
            cv2.imshow('MainWindow', img_copy)
            cv2.waitKey(delay)

        # 最後顯示完整的文字
        img_pil = Image.fromarray(img.copy())
        draw = ImageDraw.Draw(img_pil)
        for i, char in enumerate(text1):
            draw.text((current_x1 + i * (font_size + Ui_Game_Start.letter_spacing), positions[0][1]), char, font=font, fill=(0, 0, 0))
        for i, char in enumerate(text2):
            draw.text((current_x2 + i * (font_size + Ui_Game_Start.letter_spacing), positions[1][1]), char, font=font, fill=(0, 0, 0))
        img_copy = np.array(img_pil)
        cv2.imshow('MainWindow', img_copy)

    # 文字特效2
    def makeTextZoomEffect(img, text1, text2, positions, font_path, delay):
        """顯示縮放效果的文字，並增加字間距。"""
        font_size_start = 10
        font_size_end = 38
        steps = max(len(text1), len(text2))

        for step in range(steps + 1):
            img_pil = Image.fromarray(img.copy())
            draw = ImageDraw.Draw(img_pil)

            # 第一行文字
            if step <= len(text1):
                font = ImageFont.truetype(font_path, font_size_start + (font_size_end - font_size_start) * step // steps)
                current_x1 = (img.shape[1] - (len(text1[:step]) * (font.size + Ui_Game_Start.letter_spacing))) // 2
                for i, char in enumerate(text1[:step]):
                    draw.text((current_x1 + i * (font.size + Ui_Game_Start.letter_spacing), positions[0][1]), char, font=font, fill=(0, 0, 0))

            # 第二行文字
            if step <= len(text2):
                font = ImageFont.truetype(font_path, font_size_start + (font_size_end - font_size_start) * step // steps)
                current_x2 = (img.shape[1] - (len(text2[:step]) * (font.size + Ui_Game_Start.letter_spacing))) // 2
                for i, char in enumerate(text2[:step]):
                    draw.text((current_x2 + i * (font.size + Ui_Game_Start.letter_spacing), positions[1][1]), char, font=font, fill=(0, 0, 0))

            img_copy = np.array(img_pil)
            cv2.imshow('MainWindow', img_copy)
            cv2.waitKey(delay)

        # 最後顯示完整的文字
        img_pil = Image.fromarray(img.copy())
        draw = ImageDraw.Draw(img_pil)
        for i, char in enumerate(text1):
            draw.text((current_x1 + i * (font.size + Ui_Game_Start.letter_spacing), positions[0][1]), char, font=font, fill=(0, 0, 0))
        for i, char in enumerate(text2):
            draw.text((current_x2 + i * (font.size + Ui_Game_Start.letter_spacing), positions[1][1]), char, font=font, fill=(0, 0, 0))
        img_copy = np.array(img_pil)
        cv2.imshow('MainWindow', img_copy)

    # 文字特效3
    def makeTextFadeInEffect(img, text1, text2, positions, font_path, delay):
        """顯示淡入效果的文字，並增加字間距。"""
        font_size = 38
        font = ImageFont.truetype(font_path, font_size)
        alpha_start = 0
        alpha_end = 255
        steps = 10

        for step in range(steps + 1):
            alpha = alpha_start + (alpha_end - alpha_start) * step // steps

            img_pil = Image.fromarray(img.copy())
            draw = ImageDraw.Draw(img_pil)

            overlay = Image.new('RGBA', img_pil.size, (255, 255, 255, 0))
            overlay_draw = ImageDraw.Draw(overlay)

            # 第一行文字淡入
            current_x1 = (img.shape[1] - (len(text1) * (font.size + Ui_Game_Start.letter_spacing))) // 2
            for i, char in enumerate(text1):
                overlay_draw.text((current_x1 + i * (font.size + Ui_Game_Start.letter_spacing), positions[0][1]), char, font=font, fill=(0, 0, 0, alpha))

            # 第二行文字淡入
            current_x2 = (img.shape[1] - (len(text2) * (font.size + Ui_Game_Start.letter_spacing))) // 2
            for i, char in enumerate(text2):
                overlay_draw.text((current_x2 + i * (font.size + Ui_Game_Start.letter_spacing), positions[1][1]), char, font=font, fill=(0, 0, 0, alpha))

            img_with_overlay = Image.alpha_composite(img_pil.convert('RGBA'), overlay)

            img_copy = np.array(img_with_overlay.convert('RGB'))
            cv2.imshow('MainWindow', img_copy)
            cv2.waitKey(delay)

        img_pil = Image.fromarray(img.copy())
        draw = ImageDraw.Draw(img_pil)
        for i, char in enumerate(text1):
            draw.text((current_x1 + i * (font.size + Ui_Game_Start.letter_spacing), positions[0][1]), char, font=font, fill=(0, 0, 0))
        for i, char in enumerate(text2):
            draw.text((current_x2 + i * (font.size + Ui_Game_Start.letter_spacing), positions[1][1]), char, font=font, fill=(0, 0, 0))
        img_copy = np.array(img_pil)
        cv2.imshow('MainWindow', img_copy)

    # 文字特效4
    def makeTextSlideInEffect(img, text1, text2, positions, font_path, delay):
        """顯示滑入效果的文字，並增加字間距。"""
        font_size = 38
        font = ImageFont.truetype(font_path, font_size)
        steps = 10

        final_x1 = (img.shape[1] - (len(text1) * (font_size + Ui_Game_Start.letter_spacing))) // 2
        final_x2 = (img.shape[1] - (len(text2) * (font_size + Ui_Game_Start.letter_spacing))) // 2

        for step in range(steps + 1):
            img_pil = Image.fromarray(img.copy())
            draw = ImageDraw.Draw(img_pil)

            current_x1 = final_x1 - (final_x1 * (steps - step) // steps)
            current_x2 = final_x2 - (final_x2 * (steps - step) // steps)

            for i, char in enumerate(text1):
                draw.text((current_x1 + i * (font_size + Ui_Game_Start.letter_spacing), positions[0][1]), char, font=font, fill=(0, 0, 0))

            for i, char in enumerate(text2):
                draw.text((current_x2 + i * (font_size + Ui_Game_Start.letter_spacing), positions[1][1]), char, font=font, fill=(0, 0, 0))

            img_copy = np.array(img_pil)
            cv2.imshow('MainWindow', img_copy)
            cv2.waitKey(delay)

        img_pil = Image.fromarray(img.copy())
        draw = ImageDraw.Draw(img_pil)
        for i, char in enumerate(text1):
            draw.text((final_x1 + i * (font_size + Ui_Game_Start.letter_spacing), positions[0][1]), char, font=font, fill=(0, 0, 0))
        for i, char in enumerate(text2):
            draw.text((final_x2 + i * (font_size + Ui_Game_Start.letter_spacing), positions[1][1]), char, font=font, fill=(0, 0, 0))
        img_copy = np.array(img_pil)
        cv2.imshow('MainWindow', img_copy)

    # 隨機選擇一個文字特效
    def makeTextEffect(img, text, positions, font_path, delay, effect_type="typewriter"):
        if effect_type == "typewriter":
            Ui_Game_Start.makeTextTypewriterEffect(img, text, "", positions, font_path, delay)
        elif effect_type == "zoom":
            Ui_Game_Start.makeTextZoomEffect(img, text, "", positions, font_path, delay)
        elif effect_type == "fade_in":
            Ui_Game_Start.makeTextFadeInEffect(img, text, "", positions, font_path, delay)
        elif effect_type == "slide_in":
            Ui_Game_Start.makeTextSlideInEffect(img, text, "", positions, font_path, delay)
        else:
            print(f"沒有找到類別: {effect_type}")

    def updateImage(self, img_array):
        """Convert image array to QPixmap and display it in QLabel."""
        # 檢查通道
        height, width, channel = img_array.shape
        
        # 如果是 BGR 格式，轉換為 RGB
        if channel == 3:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        
        # 如果是浮點數，轉換為整數型
        if img_array.dtype == np.float32:
            img_array = (img_array * 255).astype(np.uint8)

        bytes_per_line = 3 * width
        q_img = QtGui.QImage(img_array.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(q_img)
        self.video_label.setPixmap(pixmap)

    def showTextDrop(self, font_path, bg_path):
        # 設置字體大小與字間距
        font_size = 36
        letter_spacing = 40 # 調整字間距的參數

        # 背景圖片
        bg_img = cv2.imread(bg_path)
        if bg_img is None:
            print("Failed to load background image")
            return
        else:
            print("Background image loaded successfully")

        bg_img = cv2.resize(bg_img, (800, 600))  # 調整背景大小

        # 手勢圖片
        icons = []
        icon_paths = [
            'Pic/icon1.png', 
            'Pic/icon2.png', 
            'Pic/icon3.png', 
            'Pic/icon4.png'
        ]

        # 加載並調整圖標大小
        for icon_path in icon_paths:
            icon = cv2.imread(icon_path, cv2.IMREAD_UNCHANGED)
            if icon is not None:
                icon = cv2.resize(icon, (80, 80))
                icons.append(icon)
            else:
                print(f"Failed to load icon: {icon_path}")

        # 圖片的擺放位置 
        icon_positions = [
            (270, 320), 
            (270, 420), 
            (430, 320), 
            (430, 420)
        ]
        
        # 顯示圖標在背景圖像上
        for icon, (x, y) in zip(icons, icon_positions):
            if icon.shape[2] == 4:  # 檢查圖標是否有 alpha 通道
                alpha_icon = icon[:, :, 3] / 255.0
                for c in range(0, 3):
                    bg_img[y:y + icon.shape[0], x:x + icon.shape[1], c] = (
                        alpha_icon * icon[:, :, c] + (1 - alpha_icon) * bg_img[y:y + icon.shape[0], x:x + icon.shape[1], c]
                    )
            else:
                bg_img[y:y + icon.shape[0], x:x + icon.shape[1]] = icon[:, :, :3]
        
        # 初始化題號
        question_number = 1
        countdown_time = 30  # 改成總時常360秒
        start_time = time.time()

        while True:
            topic, typo, typo_position = Ui_Game_Start.Display_Random_Topic()

            # 當題目、錯字或錯字位置無效時，不遞增題號
            if not topic or not typo or typo_position == "":
                continue  # 跳過此題並保留當前題號

            # 顯示題目並遞增題號
            topic_number_text = f"第 {question_number} 題"
            question_number += 1

            # 設置選項：隨機選擇並隨機排序
            correct_answer = typo[0]
            typo_options = list(typo[1:])
            random_typo = random.choice(typo_options)
            topic_with_typo = list(topic)

            if int(typo_position) < len(topic_with_typo):
                topic_with_typo[int(typo_position)] = random_typo
            topic_with_typo = ''.join(topic_with_typo)

            # 構建選項
            typo_choices = [correct_answer] + [char for char in typo_options if char != random_typo]
            typo_choices = random.sample(typo_choices, min(4, len(typo_choices)))

            # 設置選項顯示位置
            option_positions = [
                (270, 300), 
                (270, 400), 
                (430, 300), 
                (430, 400)
            ]

            img_pil = Image.fromarray(bg_img)
            draw = ImageDraw.Draw(img_pil)
            font = ImageFont.truetype(font_path, 36)

            draw.text((20, 20), topic_number_text, font=font, fill=(0, 0, 0))
            elapsed_time = int(time.time() - start_time)
            remaining_time = max(0, countdown_time - elapsed_time)
            countdown_text = f"時間: {remaining_time}"
            draw.text((600, 20), countdown_text, font=font, fill=(255, 0, 0))

            start_x = (bg_img.shape[1] - len(topic_with_typo) * (font_size + letter_spacing)) // 2
            for i, char in enumerate(topic_with_typo):
                x_position = start_x + i * (font_size + letter_spacing)
                y_position = 200
                if i == int(typo_position):
                    box_top_left = (x_position - 5, y_position - 5)
                    box_bottom_right = (x_position + font_size + 5, y_position + font_size + 5)
                    draw.rectangle([box_top_left, box_bottom_right], outline=(0, 0, 255), width=3)
                draw.text((x_position, y_position), char, font=font, fill=(0, 0, 0))

            for (x, y), choice in zip(option_positions, typo_choices):
                draw.text((x, y), choice, font=font, fill=(0, 0, 0))

            img_copy = np.array(img_pil)
            self.updateImage(img_copy)

            # if remaining_time <= 0:
            #     print("Time's up! Proceeding to the next question.")
            #     break

            # key = cv2.waitKey(1000)
            # if key == 27 or remaining_time <= 0:
            #     break
            if remaining_time <= 0:
                    print("時間到，進入下一題")
                    break

            key = cv2.waitKey(1000)
            if key == 27:
                    break
            elif key == ord('q') or key == ord('Q'):
                    cv2.destroyAllWindows()
                    return
            

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_Game_Start()
    window.show()
    font_path = 'Font/NaikaiFont-Bold.ttf'
    bg_path = 'Font/game.jpg'
    window.showTextDrop(font_path, bg_path)
    sys.exit(app.exec_())

