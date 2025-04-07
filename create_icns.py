"""
生成macOS应用图标
"""
import os
import sys

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from PIL import Image
from app_icon import create_app_icon

def create_icns():
    # 创建临时目录
    iconset_dir = "resources/app.iconset"
    os.makedirs(iconset_dir, exist_ok=True)
    
    # 生成基础图标
    icon = create_app_icon(size=1024)  # 使用最大尺寸
    
    # 生成不同尺寸的图标
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    for size in sizes:
        # 普通分辨率
        resized = icon.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(f"{iconset_dir}/icon_{size}x{size}.png")
        
        # 高分辨率 (@2x)
        if size <= 512:
            resized = icon.resize((size * 2, size * 2), Image.Resampling.LANCZOS)
            resized.save(f"{iconset_dir}/icon_{size}x{size}@2x.png")
    
    # 使用 iconutil 将 iconset 转换为 icns
    os.system(f"iconutil -c icns resources/app.iconset")
    
    # 清理临时文件
    os.system("rm -rf resources/app.iconset")
    
    # 确保生成的图标文件名与setup.py中的配置匹配
    if os.path.exists("resources/app_icon.icns"):
        os.remove("resources/app_icon.icns")
    # 不需要重命名，直接生成为app.icns

if __name__ == "__main__":
    create_icns() 