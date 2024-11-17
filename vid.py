from moviepy.editor import VideoFileClip
import os

# 確認影片檔案路徑
video_path = "C:/mypython4/pack/test/Screen/video/my_video.mp4"  # 確保這裡指向的是影片檔案
print("影片路徑存在:", os.path.exists(video_path))  # 檢查路徑是否存在

# 嘗試載入影片檔案
try:
    clip = VideoFileClip(video_path)
    print("影片讀取成功")
except Exception as e:
    print("影片讀取失敗:", e)
