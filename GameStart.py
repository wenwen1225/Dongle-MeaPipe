import random
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image, ImageEnhance
import mysql.connector as db
import os
import time  # 用於倒數計時
from PIL import ImageFont, ImageDraw, Image

def Get_Config():
    config = {}
    # 獲取當前腳本的目錄
    base_dir = os.path.dirname(__file__)  # 這會獲取當前腳本的絕對路徑
    # 將目錄回到 Data 文件夾
    config_path = os.path.join(base_dir,  'Data', 'config.txt')
    
    with open(config_path, 'r') as f:
        for line in f:
            key, value = line.strip().split('=')
            config[key.strip()] = value.strip()
    
    return config

def Display_Random_Topic():
    try:
        config = Get_Config()
        connect = db.connect(
            host=config['host'],
            user=config['user'],
            password=config.get('password', ''),
            database=config['database']
        )
        cursor = connect.cursor()

        # 查詢 '題目'、'錯字' 和 '錯字位置' 列
        query = "SELECT 題目, 錯字, 錯字位置 FROM topic;"
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            # 隨機選擇一行
            random_row = random.choice(rows)
            topic = random_row[0] or ""  # SQL資料表中題目那一欄
            typo = random_row[1] or ""   # SQL資料表中錯字那一欄
            typo_position = str(random_row[2] or "")  # 保持 typo_position 為字串

            # 確保錯字不超過四個
            if len(typo) > 5:
                typo = typo[:4]  # 限制錯字長度

            return topic, typo, typo_position  # 返回 '題目'、'錯字' 和 '錯字位置'
        else:
            print("没有找到")
            return "", "", ""
        
    except db.Error as error:
        print("執行查詢時出現錯誤:", error)
        return "", "", ""
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connect' in locals():
            connect.close()

letter_spacing = 40

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
            current_x1 = (img.shape[1] - (len(text1[:step]) * (font_size + letter_spacing))) // 2  # 置中並計算字間距
            for i, char in enumerate(text1[:step]):
                draw.text((current_x1 + i * (font_size + letter_spacing), positions[0][1]), char, font=font, fill=(0, 0, 0))

        # 第二行文字
        if step <= len(text2):
            current_x2 = (img.shape[1] - (len(text2[:step]) * (font_size + letter_spacing))) // 2  # 置中並計算字間距
            for i, char in enumerate(text2[:step]):
                draw.text((current_x2 + i * (font_size + letter_spacing), positions[1][1]), char, font=font, fill=(0, 0, 0))

        img_copy = np.array(img_pil)
        cv2.imshow('MainWindow', img_copy)
        cv2.waitKey(delay)

    # 最後顯示完整的文字
    img_pil = Image.fromarray(img.copy())
    draw = ImageDraw.Draw(img_pil)
    for i, char in enumerate(text1):
        draw.text((current_x1 + i * (font_size + letter_spacing), positions[0][1]), char, font=font, fill=(0, 0, 0))
    for i, char in enumerate(text2):
        draw.text((current_x2 + i * (font_size + letter_spacing), positions[1][1]), char, font=font, fill=(0, 0, 0))
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
            current_x1 = (img.shape[1] - (len(text1[:step]) * (font.size + letter_spacing))) // 2  # 置中並計算字間距
            for i, char in enumerate(text1[:step]):
                draw.text((current_x1 + i * (font.size + letter_spacing), positions[0][1]), char, font=font, fill=(0, 0, 0))

        # 第二行文字
        if step <= len(text2):
            font = ImageFont.truetype(font_path, font_size_start + (font_size_end - font_size_start) * step // steps)
            current_x2 = (img.shape[1] - (len(text2[:step]) * (font.size + letter_spacing))) // 2  # 置中並計算字間距
            for i, char in enumerate(text2[:step]):
                draw.text((current_x2 + i * (font.size + letter_spacing), positions[1][1]), char, font=font, fill=(0, 0, 0))

        img_copy = np.array(img_pil)
        cv2.imshow('MainWindow', img_copy)
        cv2.waitKey(delay)

    # 最後顯示完整的文字
    img_pil = Image.fromarray(img.copy())
    draw = ImageDraw.Draw(img_pil)
    for i, char in enumerate(text1):
        draw.text((current_x1 + i * (font.size + letter_spacing), positions[0][1]), char, font=font, fill=(0, 0, 0))
    for i, char in enumerate(text2):
        draw.text((current_x2 + i * (font.size + letter_spacing), positions[1][1]), char, font=font, fill=(0, 0, 0))
    img_copy = np.array(img_pil)
    cv2.imshow('MainWindow', img_copy)

# 文字特效3
def makeTextFadeInEffect(img, text1, text2, positions, font_path, delay):
    """顯示淡入效果的文字，並增加字間距。"""
    font_size = 38
    font = ImageFont.truetype(font_path, font_size)
    alpha_start = 0
    alpha_end = 255
    steps = 10  # 控制淡入的過程

    for step in range(steps + 1):
        alpha = alpha_start + (alpha_end - alpha_start) * step // steps

        img_pil = Image.fromarray(img.copy())
        draw = ImageDraw.Draw(img_pil)

        overlay = Image.new('RGBA', img_pil.size, (255, 255, 255, 0))
        overlay_draw = ImageDraw.Draw(overlay)

        # 第一行文字淡入
        current_x1 = (img.shape[1] - (len(text1) * (font.size + letter_spacing))) // 2  # 置中並計算字間距
        for i, char in enumerate(text1):
            overlay_draw.text((current_x1 + i * (font.size + letter_spacing), positions[0][1]), char, font=font, fill=(0, 0, 0, alpha))

        # 第二行文字淡入
        current_x2 = (img.shape[1] - (len(text2) * (font.size + letter_spacing))) // 2  # 置中並計算字間距
        for i, char in enumerate(text2):
            overlay_draw.text((current_x2 + i * (font.size + letter_spacing), positions[1][1]), char, font=font, fill=(0, 0, 0, alpha))

        # 合併圖層
        img_with_overlay = Image.alpha_composite(img_pil.convert('RGBA'), overlay)

        # 顯示最終效果
        img_copy = np.array(img_with_overlay.convert('RGB'))
        cv2.imshow('MainWindow', img_copy)
        cv2.waitKey(delay)

    # 最後顯示完整的文字
    img_pil = Image.fromarray(img.copy())
    draw = ImageDraw.Draw(img_pil)
    for i, char in enumerate(text1):
        draw.text((current_x1 + i * (font.size + letter_spacing), positions[0][1]), char, font=font, fill=(0, 0, 0))
    for i, char in enumerate(text2):
        draw.text((current_x2 + i * (font.size + letter_spacing), positions[1][1]), char, font=font, fill=(0, 0, 0))
    img_copy = np.array(img_pil)
    cv2.imshow('MainWindow', img_copy)

# 文字特效4
def makeTextSlideInEffect(img, text1, text2, positions, font_path, delay):
    """顯示滑入效果的文字，並增加字間距。"""
    font_size = 38
    font = ImageFont.truetype(font_path, font_size)
    steps = 10  # 滑入步驟

    # 計算最後文字位置的 x 座標
    final_x1 = (img.shape[1] - (len(text1) * (font_size + letter_spacing))) // 2
    final_x2 = (img.shape[1] - (len(text2) * (font_size + letter_spacing))) // 2

    for step in range(steps + 1):
        img_pil = Image.fromarray(img.copy())
        draw = ImageDraw.Draw(img_pil)

        # 根據步驟計算當前位置
        current_x1 = final_x1 - (final_x1 * (steps - step) // steps)
        current_x2 = final_x2 - (final_x2 * (steps - step) // steps)

        # 第一行文字滑入
        for i, char in enumerate(text1):
            draw.text((current_x1 + i * (font_size + letter_spacing), positions[0][1]), char, font=font, fill=(0, 0, 0))

        # 第二行文字滑入
        for i, char in enumerate(text2):
            draw.text((current_x2 + i * (font_size + letter_spacing), positions[1][1]), char, font=font, fill=(0, 0, 0))

        img_copy = np.array(img_pil)
        cv2.imshow('MainWindow', img_copy)
        cv2.waitKey(delay)

    # 最後顯示完整的文字
    img_pil = Image.fromarray(img.copy())
    draw = ImageDraw.Draw(img_pil)
    for i, char in enumerate(text1):
        draw.text((final_x1 + i * (font_size + letter_spacing), positions[0][1]), char, font=font, fill=(0, 0, 0))
    for i, char in enumerate(text2):
        draw.text((final_x2 + i * (font_size + letter_spacing), positions[1][1]), char, font=font, fill=(0, 0, 0))
    img_copy = np.array(img_pil)
    cv2.imshow('MainWindow', img_copy)

text_effects = {
    'typewriter': makeTextTypewriterEffect,
    'zoom': makeTextZoomEffect,
    'fade_in': makeTextFadeInEffect,
    'slide_in': makeTextSlideInEffect
}

# 在 showTextDrop 函數中顯示錯字的位置 顯示題目的主函數
def showTextDrop(font_path, bg_path):
    # 設置字體大小與字間距
    font_size = 36
    letter_spacing = 40  # 調整字間距的參數

    # 背景圖片
    bg_img = cv2.imread(bg_path)
    if bg_img is None:
        print("Error: Could not open background image.")
        return
    else:
        print("Background image loaded successfully.")

    bg_img = cv2.resize(bg_img, (800, 600))  # 調整背景大小

    # 加載圖標
    icons = []
    icon_paths = [
        'Pic/icon1.png',
        'Pic/icon2.png',
        'Pic/icon3.png',
        'Pic/icon4.png'
    ]

    # 加載並調整圖標大小
    for icon_path in icon_paths:
        icon = cv2.imread(icon_path, cv2.IMREAD_UNCHANGED)  # 支援透明度
        if icon is not None:
            icon = cv2.resize(icon, (80, 80))  # 調整圖標大小
            icons.append(icon)
        else:
            print(f"Error: Could not load icon at {icon_path}")

    # 計算圖標的擺放位置
    icon_positions = [
        (270, 320),  # icon1
        (270, 420),  # icon2
        (430, 320),  # icon3
        (430, 420)   # icon4
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
    countdown_time = 30  # 改成總時常300秒
    start_time = time.time()

    while True:
        topic, typo, typo_position = Display_Random_Topic()

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
            (270, 300),  # icon1 上方
            (270, 400),  # icon2 下方
            (430, 300),  # icon3 上方
            (430, 400)   # icon4 下方
        ]

        # 選擇並執行文字特效
        effect_function = random.choice(list(text_effects.values()))
        effect_function(bg_img, topic_with_typo, "", [(200, 200), (200, 200)], font_path, delay=200)

        # 開始顯示完整題目，直到倒數完畢
        while True:
            elapsed_time = int(time.time() - start_time)
            remaining_time = max(0, countdown_time - elapsed_time)

            # 檢查倒數是否結束
            if remaining_time <= 0:
                print("時間到，結束測驗")
                cv2.destroyAllWindows()
                return  # 時間到，退出函數

            # 創建畫布
            img_pil = Image.fromarray(bg_img)
            draw = ImageDraw.Draw(img_pil)
            font = ImageFont.truetype(font_path, 36)

            # 顯示題號和倒數計時
            draw.text((20, 20), topic_number_text, font=font, fill=(0, 0, 0))
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
            cv2.imshow('MainWindow', img_copy)

            if remaining_time <= 0:
                print("時間到，跳到下一題")
                break

            key = cv2.waitKey(1000)
            if key == 27:
                break
            elif key == ord('q') or key == ord('Q'):
                cv2.destroyAllWindows()
                return

    cv2.destroyAllWindows()

# 字體文件路徑
font_path = 'Font\\NaikaiFont-Bold.ttf'
# 背景圖片路徑
bg_path = 'Font/game.jpg'

# 顯示文字效果
showTextDrop(font_path, bg_path)