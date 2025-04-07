from PIL import Image, ImageDraw, ImageFont
import os

def create_dmg_background():
    # 创建一个新的图像，使用 RGBA 模式（支持透明度）
    width = 660
    height = 400
    image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # 添加安装指引
    instructions = "将 NaviParser 拖到 Applications 文件夹安装"
    # 这里应该使用系统字体，如果没有将回退到默认字体
    try:
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 16)
    except:
        font = ImageFont.load_default()

    # 获取文本大小
    text_bbox = draw.textbbox((0, 0), instructions, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    
    # 在图像中央绘制文本
    x = (width - text_width) // 2
    y = height // 2
    draw.text((x, y), instructions, font=font, fill=(0, 0, 0, 255))

    # 确保目录存在
    os.makedirs('resources', exist_ok=True)
    
    # 保存图像
    image.save('resources/dmg_background.png', 'PNG')

if __name__ == '__main__':
    create_dmg_background() 