import random
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image, ImageEnhance
import mysql.connector as db
import os

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

        # 查詢 '題目' 和 '錯字' 列
        query = "SELECT 題目, 錯字 FROM topic;"
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            # 隨機選擇一行
            random_row = random.choice(rows)
            return random_row[0] or "", random_row[1] or ""  # 返回 '題目' 和 '錯字'
        else:
            print("没有找到")
            return "", ""
        
    except db.Error as error:
        print("執行查詢時出現錯誤:", error)
        return "", ""
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connect' in locals():
            connect.close()

# 封裝函數，隨機選擇一個動畫特效
def apply_random_animation_effect(img_path, font_path, text1, text2, delay=200):
    # 背景圖像
    img = cv2.imread(img_path)
    if img is None:
        print("Error: Could not open background image.")
        return
    else:
        img = cv2.resize(img, (800, 600))  # 調整大小

    positions = [(0, 200), (0, 250)]  # 設定文字的顯示位置

    # 隨機選擇動畫效果
    effect = random.choice(['typewriter', 'zoom', 'fade_in', 'slide_in'])
    
    if effect == 'typewriter':
        makeTextTypewriterEffect(img, text1, text2, positions, font_path, delay)
    elif effect == 'zoom':
        makeTextZoomEffect(img, text1, text2, positions, font_path, delay)
    elif effect == 'fade_in':
        makeTextFadeInEffect(img, text1, text2, positions, font_path, delay)
    elif effect == 'slide_in':
        makeTextSlideInEffect(img, text1, text2, positions, font_path, delay)

letter_spacing=30

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
                draw.text((current_x1 + i * (font_size + letter_spacing), positions[0][1]), char, font=font, fill=(255, 255, 255))

        # 第二行文字
        if step <= len(text2):
            current_x2 = (img.shape[1] - (len(text2[:step]) * (font_size + letter_spacing))) // 2  # 置中並計算字間距
            for i, char in enumerate(text2[:step]):
                draw.text((current_x2 + i * (font_size + letter_spacing), positions[1][1]), char, font=font, fill=(255, 255, 255))

        img_copy = np.array(img_pil)
        cv2.imshow('Image', img_copy)
        cv2.waitKey(delay)

    # 最後顯示完整的文字
    img_pil = Image.fromarray(img.copy())
    draw = ImageDraw.Draw(img_pil)
    for i, char in enumerate(text1):
        draw.text((current_x1 + i * (font_size + letter_spacing), positions[0][1]), char, font=font, fill=(255, 255, 255))
    for i, char in enumerate(text2):
        draw.text((current_x2 + i * (font_size + letter_spacing), positions[1][1]), char, font=font, fill=(255, 255, 255))
    img_copy = np.array(img_pil)
    cv2.imshow('Image', img_copy)


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
                draw.text((current_x1 + i * (font.size + letter_spacing), positions[0][1]), char, font=font, fill=(255, 255, 255))

        # 第二行文字
        if step <= len(text2):
            font = ImageFont.truetype(font_path, font_size_start + (font_size_end - font_size_start) * step // steps)
            current_x2 = (img.shape[1] - (len(text2[:step]) * (font.size + letter_spacing))) // 2  # 置中並計算字間距
            for i, char in enumerate(text2[:step]):
                draw.text((current_x2 + i * (font.size + letter_spacing), positions[1][1]), char, font=font, fill=(255, 255, 255))

        img_copy = np.array(img_pil)
        cv2.imshow('Image', img_copy)
        cv2.waitKey(delay)

    # 最後顯示完整的文字
    img_pil = Image.fromarray(img.copy())
    draw = ImageDraw.Draw(img_pil)
    for i, char in enumerate(text1):
        draw.text((current_x1 + i * (font.size + letter_spacing), positions[0][1]), char, font=font, fill=(255, 255, 255))
    for i, char in enumerate(text2):
        draw.text((current_x2 + i * (font.size + letter_spacing), positions[1][1]), char, font=font, fill=(255, 255, 255))
    img_copy = np.array(img_pil)
    cv2.imshow('Image', img_copy)


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
            overlay_draw.text((current_x1 + i * (font.size + letter_spacing), positions[0][1]), char, font=font, fill=(255, 255, 255, alpha))

        # 第二行文字淡入
        current_x2 = (img.shape[1] - (len(text2) * (font.size + letter_spacing))) // 2  # 置中並計算字間距
        for i, char in enumerate(text2):
            overlay_draw.text((current_x2 + i * (font.size + letter_spacing), positions[1][1]), char, font=font, fill=(255, 255, 255, alpha))

        # 合併圖層
        img_with_overlay = Image.alpha_composite(img_pil.convert('RGBA'), overlay)

        # 顯示最終效果
        img_copy = np.array(img_with_overlay.convert('RGB'))
        cv2.imshow('Image', img_copy)
        cv2.waitKey(delay)

    # 最後顯示完整的文字
    img_pil = Image.fromarray(img.copy())
    draw = ImageDraw.Draw(img_pil)
    for i, char in enumerate(text1):
        draw.text((current_x1 + i * (font.size + letter_spacing), positions[0][1]), char, font=font, fill=(255, 255, 255))
    for i, char in enumerate(text2):
        draw.text((current_x2 + i * (font.size + letter_spacing), positions[1][1]), char, font=font, fill=(255, 255, 255))
    img_copy = np.array(img_pil)
    cv2.imshow('Image', img_copy)

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
            draw.text((current_x1 + i * (font_size + letter_spacing), positions[0][1]), char, font=font, fill=(255, 255, 255))

        # 第二行文字滑入
        for i, char in enumerate(text2):
            draw.text((current_x2 + i * (font_size + letter_spacing), positions[1][1]), char, font=font, fill=(255, 255, 255))

        img_copy = np.array(img_pil)
        cv2.imshow('Image', img_copy)
        cv2.waitKey(delay)

    # 最後顯示完整的文字
    img_pil = Image.fromarray(img.copy())
    draw = ImageDraw.Draw(img_pil)
    for i, char in enumerate(text1):
        draw.text((final_x1 + i * (font_size + letter_spacing), positions[0][1]), char, font=font, fill=(255, 255, 255))
    for i, char in enumerate(text2):
        draw.text((final_x2 + i * (font_size + letter_spacing), positions[1][1]), char, font=font, fill=(255, 255, 255))
    img_copy = np.array(img_pil)
    cv2.imshow('Image', img_copy)

def showTextDrop(font_path, bg_path):
    # 背景圖片
    bg_img = cv2.imread(bg_path)
    if bg_img is None:
        print("Error: Could not open background image.")
        return
    else:
        print("Background image loaded successfully.")

    bg_img = cv2.resize(bg_img, (500, 500))  # 調整背景大小

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
        icon = cv2.imread(icon_path, cv2.IMREAD_UNCHANGED)  # Support transparency
        if icon is not None:
            icon = cv2.resize(icon, (80, 80))  # Enlarged icon size
            icons.append(icon)
        else:
            print(f"Error: Could not load icon at {icon_path}")

    # 計算圖標的擺放位置，假設在文字下方
    icon_positions = [
        (150, 320),  # icon1
        (230, 320),  # icon2
        (310, 320),  # icon3
        (390, 320)   # icon4
    ]
    
    # 顯示圖標在背景圖像上
    for icon, (x, y) in zip(icons, icon_positions):
        # 檢查圖標是否有 alpha 通道 (透明度)
        if icon.shape[2] == 4:  # 圖標有 4 個通道 (包括透明度)
            # 獲取 Alpha 通道
            alpha_icon = icon[:, :, 3] / 255.0
            # 只取 BGR 通道
            for c in range(0, 3):  # 前三個為 BGR 通道
                bg_img[y:y + icon.shape[0], x:x + icon.shape[1], c] = (
                    alpha_icon * icon[:, :, c] + (1 - alpha_icon) * bg_img[y:y + icon.shape[0], x:x + icon.shape[1], c]
                )
        else:
            # 沒有 alpha 通道，直接貼圖
            bg_img[y:y + icon.shape[0], x:x + icon.shape[1]] = icon[:, :, :3]  # 只取 BGR 通道

    # 文字
    while True:
        # 隨機題目與錯字
        topic, typo = Display_Random_Topic()
        if not topic and not typo:
            break

        # 顯示位置，y 軸位置固定
        positions = [(0, 200), (0, 250)]

        # 隨機選擇顯示效果
        effect = random.choice(['typewriter', 'zoom', 'fade_in', 'slide_in'])
        if effect == 'typewriter':
            makeTextTypewriterEffect(bg_img, topic, typo, positions, font_path, 200)
        elif effect == 'zoom':
            makeTextZoomEffect(bg_img, topic, typo, positions, font_path, 200)
        elif effect == 'fade_in':
            makeTextFadeInEffect(bg_img, topic, typo, positions, font_path, 200)
        elif effect == 'slide_in':
            makeTextSlideInEffect(bg_img, topic, typo, positions, font_path, 200)

        key = cv2.waitKey(0)  
        if key == 27:  # ESC的ASCII 碼是 27
            continue
        elif key == ord('q') or key == ord('Q'):  # 按鍵退出
            break

    cv2.destroyAllWindows()


# 字體文件路徑
font_path = 'Font\\NaikaiFont-Bold.ttf'
# 背景圖片路徑
bg_path = 'Font/game.jpg'

# 顯示文字效果
showTextDrop(font_path, bg_path) 