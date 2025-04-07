from PIL import Image, ImageDraw, ImageFont
import io

def create_app_icon(size=64):
    # 创建一个新的RGBA图像（支持透明度）
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 定义颜色
    primary_color = "#2196f3"  # Material Blue 500
    secondary_color = "#1976d2"  # Material Blue 700
    
    # 绘制圆形背景
    padding = size // 8
    circle_bbox = (padding, padding, size - padding, size - padding)
    draw.ellipse(circle_bbox, fill=primary_color)
    
    # 绘制数据库图标
    db_height = size // 3
    db_width = size - (padding * 4)
    db_x = size // 2 - db_width // 2
    db_y = size // 2 - db_height // 2
    
    # 绘制数据库的圆柱体效果
    for y in range(3):
        top_y = db_y + (y * (db_height // 3))
        bottom_y = top_y + (db_height // 3)
        
        # 绘制椭圆
        draw.ellipse(
            (db_x, top_y, db_x + db_width, bottom_y),
            fill=secondary_color,
            outline='white'
        )
        
        # 如果是顶部椭圆，添加高光效果
        if y == 0:
            highlight_width = db_width * 0.7
            highlight_x = db_x + (db_width - highlight_width) // 2
            highlight_y = top_y + 2
            draw.ellipse(
                (highlight_x, highlight_y, 
                 highlight_x + highlight_width, highlight_y + 4),
                fill='#ffffff66'  # 半透明白色
            )
    
    return image

def get_icon_bytes():
    """获取图标的字节数据"""
    image = create_app_icon()
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue() 