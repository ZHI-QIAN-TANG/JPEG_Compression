from PIL import Image

# 讀取影像
image = Image.open('test5.jpg')

# 設定壓縮品質，範圍為 0（最差品質，最大壓縮）到 100（最佳品質，最小壓縮）
quality = 50

# 儲存影像並進行 JPEG 壓縮
image.save('compressed.jpg', 'JPEG', quality=quality)