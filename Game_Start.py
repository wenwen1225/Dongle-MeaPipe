import random
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image, ImageEnhance
import mysql.connector as db
import os
import string

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
        # 從配置檔中獲取資料庫連線配置
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
            random_row = random.choice(rows)
            topic = random_row[0]  # 題目
            typo_list = list(random_row[1])  # 錯字列表
            typo_position = random_row[2]  # 錯字位置

            # 檢查錯字數量
            if len(typo_list) < 5:
                raise ValueError("錯字列表中應包含一個正確答案和四個錯字！")

            # 提取正確答案和錯字
            correct_answer = typo_list[0]
            typo_candidates = typo_list[1:]  # 錯字列表的剩餘部分

            # 隨機選擇三個錯誤選項
            error_options = random.sample(typo_candidates, min(3, len(typo_candidates)))

            # 確保錯字不會與錯誤選項重複
            if correct_answer in error_options:
                error_options.remove(correct_answer)

            # 確保始終有四個選項
            if len(error_options) < 3:
                # 如果錯字不夠，重新選擇
                error_options = random.sample(typo_candidates, 3)
            error_options.append(correct_answer)
            random.shuffle(error_options)  # 隨機排列選項

            # 從錯誤選項中選一個用來替換題目中的正確字
            typo_to_replace = random.choice(typo_candidates)

            # 替換題目中的相應字
            if 0 <= typo_position < len(topic):
                topic_list = list(topic)
                topic_list[typo_position] = typo_to_replace  # 用錯字替換正確的字
                modified_topic = ''.join(topic_list)
            else:
                modified_topic = topic

            # 返回修改後的題目、正確答案和四個選項
            return modified_topic, correct_answer, error_options
        else:
            print("没有找到任何題目")
            return "", "", []
        
    except db.Error as error:
        print("執行查詢時出現錯誤:", error)
        return "", "", []
    
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

    # 確保最終顯示完整的文字
    img_pil = Image.fromarray(img.copy())
    draw = ImageDraw.Draw(img_pil)
    for i, char in enumerate(text1):
        draw.text((current_x1 + i * (font.size + letter_spacing), positions[0][1]), char, font=font, fill=(255, 255, 255))
    for i, char in enumerate(text2):
        draw.text((current_x2 + i * (font.size + letter_spacing), positions[1][1]), char, font=font, fill=(255, 255, 255))
    img_copy = np.array(img_pil)
    # 確保最終顯示完整的文字並保持
    cv2.imshow('Image', img_copy)
    cv2.waitKey(0)  # 等待用戶按鍵操作後再結束



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

    # 確保最終顯示完整的文字
    img_pil = Image.fromarray(img.copy())
    draw = ImageDraw.Draw(img_pil)
    for i, char in enumerate(text1):
        draw.text((current_x1 + i * (font.size + letter_spacing), positions[0][1]), char, font=font, fill=(255, 255, 255))
    for i, char in enumerate(text2):
        draw.text((current_x2 + i * (font.size + letter_spacing), positions[1][1]), char, font=font, fill=(255, 255, 255))
    img_copy = np.array(img_pil)
    # 確保最終顯示完整的文字並保持
    cv2.imshow('Image', img_copy)
    cv2.waitKey(0)  # 等待用戶按鍵操作後再結束



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

    # 確保最終顯示完整的文字
    img_pil = Image.fromarray(img.copy())
    draw = ImageDraw.Draw(img_pil)
    for i, char in enumerate(text1):
        draw.text((current_x1 + i * (font.size + letter_spacing), positions[0][1]), char, font=font, fill=(255, 255, 255))
    for i, char in enumerate(text2):
        draw.text((current_x2 + i * (font.size + letter_spacing), positions[1][1]), char, font=font, fill=(255, 255, 255))
    img_copy = np.array(img_pil)
    # 確保最終顯示完整的文字並保持
    cv2.imshow('Image', img_copy)
    cv2.waitKey(0)  # 等待用戶按鍵操作後再結束


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

    # 確保最終顯示完整的文字
    img_pil = Image.fromarray(img.copy())
    draw = ImageDraw.Draw(img_pil)
    for i, char in enumerate(text1):
        draw.text((current_x1 + i * (font.size + letter_spacing), positions[0][1]), char, font=font, fill=(255, 255, 255))
    for i, char in enumerate(text2):
        draw.text((current_x2 + i * (font.size + letter_spacing), positions[1][1]), char, font=font, fill=(255, 255, 255))
    img_copy = np.array(img_pil)
    # 確保最終顯示完整的文字並保持
    cv2.imshow('Image', img_copy)
    cv2.waitKey(0)  # 等待用戶按鍵操作後再結束


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
    image_folder = r'C:\mypython4\pack\Screen\img'
    icon_paths = [
        os.path.join(image_folder, 'icon1.png'),
        os.path.join(image_folder, 'icon2.png'),
        os.path.join(image_folder, 'icon3.png'),
        os.path.join(image_folder, 'icon4.png')
    ]
    
    # 加載並調整圖標大小
    for icon_path in icon_paths:
        icon = cv2.imread(icon_path, cv2.IMREAD_UNCHANGED)  # 支持透明
        if icon is not None:
            icon = cv2.resize(icon, (80, 80))  # 圖標大小
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
        if icon.shape[2] == 4:  # 圖標有 4 個通道 (包括透明度)
            alpha_icon = icon[:, :, 3] / 255.0
            for c in range(0, 3):  # 前三個為 BGR 通道
                bg_img[y:y + icon.shape[0], x:x + icon.shape[1], c] = (
                    alpha_icon * icon[:, :, c] + (1 - alpha_icon) * bg_img[y:y + icon.shape[0], x:x + icon.shape[1], c]
                )
        else:
            bg_img[y:y + icon.shape[0], x:x + icon.shape[1]] = icon[:, :, :3]  # 只取 BGR 通道

    while True:
        # 隨機題目與錯字
        topic, correct_answer, error_options = Display_Random_Topic()
        if not topic and not correct_answer:
            break

        # 顯示位置，y 軸位置固定
        positions = [(0, 200), (0, 250)]  # 固定的文字位置

        # 顯示題目
        bg_img_copy = bg_img.copy()  # 保存背景图像的副本
        effect = random.choice(['typewriter', 'zoom', 'fade_in', 'slide_in'])
        
        # 根据效果显示题目
        if effect == 'typewriter':
            makeTextTypewriterEffect(bg_img_copy, topic, correct_answer, positions, font_path, 200)
        elif effect == 'zoom':
            makeTextZoomEffect(bg_img_copy, topic, correct_answer, positions, font_path, 200)
        elif effect == 'fade_in':
            makeTextFadeInEffect(bg_img_copy, topic, correct_answer, positions, font_path, 200)
        elif effect == 'slide_in':
            makeTextSlideInEffect(bg_img_copy, topic, correct_answer, positions, font_path, 200)

        # 顯示題目後的背景圖像
        cv2.imshow('Image', bg_img_copy)

        # 顯示錯誤選項
        option_positions = [(50, 400), (150, 400), (250, 400), (350, 400)]  # 确保选项不重叠并在图像内

        # 使用 PIL 繪製文字，替代 cv2.putText
        for i, option in enumerate(error_options):
            bg_img_copy = draw_text_with_pil(bg_img_copy, option, option_positions[i], font_path, font_size=30, color=(255, 255, 255))

        # 更新背景圖像以顯示選項
        cv2.imshow('Image', bg_img_copy)

        # 檢查按鍵事件
        key = cv2.waitKey(200)  # 等待200毫秒
        if key == 27:  # ESC的ASCII 碼是 27
            continue
        elif key == ord('q') or key == ord('Q'):  # 按鍵退出
            break

    cv2.destroyAllWindows()

def draw_text_with_pil(image, text, position, font_path, font_size=30, color=(255, 255, 255)):
    """
    使用 PIL 在 OpenCV 圖像上繪製文字。
    
    :param image: OpenCV 圖像
    :param text: 要顯示的文字
    :param position: 文字的顯示位置 (x, y)
    :param font_path: 字體檔案的路徑
    :param font_size: 字體大小
    :param color: 文字顏色，格式為 (R, G, B)
    :return: 繪製完文字的圖像
    """
    # 將 OpenCV 圖像轉換為 PIL 圖像
    img_pil = Image.fromarray(image)
    draw = ImageDraw.Draw(img_pil)
    
    # 設定字體
    font = ImageFont.truetype(font_path, font_size)
    
    # 繪製文字
    draw.text(position, text, font=font, fill=color)
    
    # 將 PIL 圖像轉換回 OpenCV 格式
    image_with_text = np.array(img_pil)
    
    return image_with_text


# 字體文件路徑
font_path = 'Font\\NaikaiFont-Bold.ttf'
# 背景圖片路徑
bg_path = 'Font/game.jpg'

# 顯示文字效果
showTextDrop(font_path, bg_path) 