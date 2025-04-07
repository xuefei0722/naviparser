"""
NaviParser - 一个用于解析 Navicat 配置文件的工具
"""

from setuptools import setup
import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join('src'))

APP = ['src/naviparser.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'site_packages': True,
    'packages': ['tkinter', 'PIL', 'cryptography'],
    'includes': [
        'password_decoder',
        'app_icon',
    ],
    'excludes': ['test', 'tests', 'pygame', 'numpy', 'pandas'],
    'iconfile': 'resources/app.icns',
    'strip': False,
    'optimize': 0,
    'frameworks': ['libffi.8.dylib', 'libcrypto.3.dylib', 'libssl.3.dylib'],
    'dylib_excludes': ['libSystem.B.dylib'],
    'plist': {
        'CFBundleName': 'NaviParser',
        'CFBundleDisplayName': 'NaviParser',
        'CFBundleIdentifier': 'com.xuefei.naviparser',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.10.0',
    }
}

setup(
    app=APP,
    name='NaviParser',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
        'cryptography',
        'pillow',
    ],
)