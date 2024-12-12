from PIL import Image

def compress_image(input_image_path, output_image_path, quality=85):
    """
    壓縮 JPEG 圖片的函式
    
    :param input_image_path: 原始圖片路徑
    :param output_image_path: 壓縮後圖片的保存路徑
    :param quality: 壓縮質量，範圍從 1 (最差) 到 95 (最佳)，默認為 85
    """
    # 開啟圖片
    with Image.open(input_image_path) as img:
        # 將圖片壓縮並保存
        img.save(output_image_path, "JPEG", quality=quality)

# 測試函式
input_image_path = "test300-300PNG.png"  # 替換為你的原始圖片路徑
output_image_path = "output_compressed.jpg"  # 替換為你要保存的壓縮圖片路徑
compress_image(input_image_path, output_image_path, quality=70)  # quality 可調整
