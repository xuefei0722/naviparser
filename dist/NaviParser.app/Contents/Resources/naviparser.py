import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import xml.etree.ElementTree as ET
import os
import base64
import io
from PIL import Image, ImageTk
from password_decoder import NavicatPasswordDecoder
from app_icon import create_app_icon

class ModernButton(ttk.Button):
    """现代风格按钮"""
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        
    def on_enter(self, e):
        self.state(['pressed'])
        
    def on_leave(self, e):
        self.state(['!pressed'])

class NavicatParser:
    def __init__(self):
        try:
            self.window = tk.Tk()
            self.window.title("NaviParser")
            print("窗口创建成功")
            
            # 创建菜单栏
            self.create_menu()
            print("菜单创建成功")
            
            # 获取屏幕尺寸
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            print(f"获取到屏幕尺寸: {screen_width}x{screen_height}")
            
            # 设置窗口初始大小为屏幕的85%
            window_width = int(screen_width * 0.85)
            window_height = int(screen_height * 0.85)
            
            # 计算窗口位置，使其居中显示
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            
            # 设置窗口大小和位置
            self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
            # 定义颜色常量
            self.DARK_BG = '#15171E'  # 更深邃的背景色
            self.DARKER_BG = '#0F1117'  # 更暗的背景色
            self.BLUE_GRADIENT_START = '#4B91F1'  # 渐变蓝起始色
            self.BLUE_GRADIENT_END = '#367BE3'  # 渐变蓝结束色
            self.LIGHT_TEXT = '#FFFFFF'  # 亮色文本
            self.GRAY_TEXT = '#8C96A6'  # 柔和的灰色文本
            self.BORDER_COLOR = '#2A2E3A'  # 边框颜色
            
            # 深色主题背景色
            self.window.configure(bg=self.DARK_BG)
            
            # 创建自定义样式
            self.create_styles()
            
            # 设置应用图标
            try:
                self.set_app_icon()
            except Exception as e:
                print(f"设置图标时出错: {e}")
            
            # 创建主容器
            self.container = ttk.Frame(self.window, style='Container.TFrame')
            self.container.grid(row=0, column=0, sticky="nsew", padx=35, pady=35)
            
            # 创建标题栏
            self.create_title_bar()
            
            # 创建主框架
            self.main_frame = ttk.Frame(self.container, style='Main.TFrame')
            self.main_frame.grid(row=1, column=0, sticky="nsew", pady=(25, 0))
            
            # 创建按钮和文本框
            self.create_widgets()
            
            # 创建表格
            self.create_treeview()
            
            # 创建状态栏
            self.create_status_bar()
            
            # 配置窗口大小调整
            self.window.columnconfigure(0, weight=1)
            self.window.rowconfigure(0, weight=1)
            self.container.columnconfigure(0, weight=1)
            self.container.rowconfigure(1, weight=1)
            self.main_frame.columnconfigure(1, weight=1)  # 文件路径标签列自动扩展
            self.main_frame.rowconfigure(1, weight=1)
            
            # 设置最小窗口大小
            min_width = int(screen_width * 0.6)  # 最小宽度为屏幕的60%
            min_height = int(screen_height * 0.6)  # 最小高度为屏幕的60%
            self.window.minsize(min_width, min_height)
            
            # 绑定窗口大小改变事件
            self.window.bind('<Configure>', self.on_window_resize)
            
        except Exception as e:
            print(f"初始化时出错: {str(e)}")
            raise  # 重新抛出异常以便查看完整的堆栈跟踪
        
    def create_styles(self):
        style = ttk.Style()
        
        # 容器样式
        style.configure('Container.TFrame', background=self.DARK_BG)
        style.configure('Main.TFrame', background=self.DARK_BG)
        
        # 标题栏样式
        style.configure(
            'Title.TLabel',
            background=self.DARK_BG,
            foreground=self.LIGHT_TEXT,
            font=('SF Pro Display', 28, 'bold')  # 增大标题字号
        )
        style.configure(
            'Version.TLabel',
            background=self.DARK_BG,
            foreground=self.GRAY_TEXT,
            font=('SF Pro Display', 12)
        )
        
        # 按钮样式
        style.configure(
            'Modern.TButton',
            background=self.BLUE_GRADIENT_START,
            foreground=self.LIGHT_TEXT,
            padding=(35, 16),  # 增加按钮内边距
            font=('SF Pro Display', 13, 'bold'),  # 加粗按钮文字
            borderwidth=0
        )
        style.map(
            'Modern.TButton',
            background=[('pressed', self.BLUE_GRADIENT_END), ('active', self.BLUE_GRADIENT_START)],
            foreground=[('pressed', self.LIGHT_TEXT), ('active', self.LIGHT_TEXT)]
        )
        
        # 表格样式
        style.configure(
            'Modern.Treeview',
            background=self.DARKER_BG,
            foreground=self.LIGHT_TEXT,
            fieldbackground=self.DARKER_BG,
            rowheight=48,  # 增加行高
            borderwidth=1,  # 添加细边框
            font=('SF Pro Display', 13)
        )
        style.configure(
            'Modern.Treeview.Heading',
            background=self.DARK_BG,
            foreground=self.GRAY_TEXT,
            padding=(20, 14),  # 增加表头内边距
            font=('SF Pro Display', 13, 'bold'),
            borderwidth=0
        )
        style.map(
            'Modern.Treeview',
            background=[('selected', self.BLUE_GRADIENT_START)],
            foreground=[('selected', self.LIGHT_TEXT)]
        )
        style.map(
            'Modern.Treeview.Heading',
            background=[('active', self.DARK_BG)],
            foreground=[('active', self.LIGHT_TEXT)]
        )
        
        # 标签样式
        style.configure(
            'Info.TLabel',
            background=self.DARK_BG,
            foreground=self.GRAY_TEXT,
            font=('SF Pro Display', 13)
        )
        
        # 状态栏样式
        style.configure(
            'Status.TFrame',
            background=self.DARKER_BG,
            borderwidth=1,  # 添加上边框
            relief='solid'  # 实线边框
        )
        style.configure(
            'Status.TLabel',
            background=self.DARKER_BG,
            foreground=self.GRAY_TEXT,
            font=('SF Pro Display', 12)
        )
        
        # 滚动条样式
        style.configure(
            'Modern.Vertical.TScrollbar',
            background=self.DARKER_BG,
            troughcolor=self.DARK_BG,
            borderwidth=0,
            arrowsize=0,
            relief='flat'
        )
        style.configure(
            'Modern.Horizontal.TScrollbar',
            background=self.DARKER_BG,
            troughcolor=self.DARK_BG,
            borderwidth=0,
            arrowsize=0,
            relief='flat'
        )
        style.map(
            'Modern.Vertical.TScrollbar',
            background=[('pressed', self.BLUE_GRADIENT_END), ('active', self.BLUE_GRADIENT_START)]
        )
        style.map(
            'Modern.Horizontal.TScrollbar',
            background=[('pressed', self.BLUE_GRADIENT_END), ('active', self.BLUE_GRADIENT_START)]
        )

    def create_title_bar(self):
        """创建标题栏"""
        title_frame = ttk.Frame(self.container, style='Main.TFrame')
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 35))
        
        # 标题
        title_label = ttk.Label(
            title_frame,
            text="NaviParser",
            style='Title.TLabel'
        )
        title_label.pack(side="left", padx=15)
        
        # 版本号
        version_label = ttk.Label(
            title_frame,
            text="v1.0.0",
            style='Version.TLabel'
        )
        version_label.pack(side="right", padx=15)
        
    def create_widgets(self):
        # 文件选择按钮
        self.select_button = ModernButton(
            self.main_frame, 
            text="选择Navicat配置文件", 
            command=self.select_file,
            style='Modern.TButton'
        )
        self.select_button.grid(row=0, column=0, sticky="w", padx=15, pady=(0, 35))
        
        # 文件路径显示
        self.file_path_var = tk.StringVar()
        self.file_path_label = ttk.Label(
            self.main_frame, 
            textvariable=self.file_path_var,
            style='Info.TLabel'
        )
        self.file_path_label.grid(row=0, column=1, sticky="w", padx=15)
        
    def create_treeview(self):
        # 创建表格容器框架
        self.tree_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        self.tree_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=15)
        
        # 创建表格
        columns = ("连接名", "主机", "端口", "用户名", "加密密码", "解密密码", "数据库类型")
        self.tree = ttk.Treeview(
            self.tree_frame, 
            columns=columns, 
            show="headings",
            style='Modern.Treeview'
        )
        
        # 设置列标题
        for col in columns:
            self.tree.heading(col, text=col)
        
        # 初始化列宽
        self.update_column_widths()
            
        # 添加滚动条
        scrollbar_y = ttk.Scrollbar(
            self.tree_frame, 
            orient=tk.VERTICAL, 
            command=self.tree.yview,
            style='Modern.Vertical.TScrollbar'
        )
        scrollbar_x = ttk.Scrollbar(
            self.tree_frame, 
            orient=tk.HORIZONTAL, 
            command=self.tree.xview,
            style='Modern.Horizontal.TScrollbar'
        )
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # 放置表格和滚动条
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        # 配置树形框架的网格权重
        self.tree_frame.columnconfigure(0, weight=1)
        self.tree_frame.rowconfigure(0, weight=1)
        
        # 绑定双击事件
        self.tree.bind('<Double-1>', self.on_double_click)
        
        # 创建提示标签
        self.tip_label = ttk.Label(
            self.main_frame,
            text="💡 提示：双击密码可以快速复制到剪贴板",
            style='Info.TLabel'
        )
        self.tip_label.grid(row=2, column=0, columnspan=2, pady=25, padx=15, sticky="w")
        
    def create_status_bar(self):
        """创建状态栏"""
        self.status_frame = ttk.Frame(self.container, style='Status.TFrame')
        self.status_frame.grid(row=2, column=0, sticky="ew", pady=(30, 0))
        
        self.status_label = ttk.Label(
            self.status_frame,
            text="就绪",
            style='Status.TLabel'
        )
        self.status_label.pack(side="left", padx=20, pady=14)
        
    def set_app_icon(self):
        icon_image = create_app_icon()
        icon_photo = ImageTk.PhotoImage(icon_image)
        self.window.iconphoto(True, icon_photo)
        self.icon_photo = icon_photo
        
    def on_double_click(self, event):
        # 获取点击的项目
        item = self.tree.identify('item', event.x, event.y)
        if not item:
            return
            
        # 获取点击的列
        column = self.tree.identify('column', event.x, event.y)
        column_id = int(column[1]) - 1  # 列索引从1开始
        
        # 只处理加密密码和解密密码列的双击
        if column_id in [4, 5]:  # 4是加密密码列，5是解密密码列
            value = self.tree.item(item)['values'][column_id]
            if value:
                self.window.clipboard_clear()
                self.window.clipboard_append(value)
                self.show_copy_tooltip(f"已复制: {value}")
                
    def show_copy_tooltip(self, text):
        x = self.window.winfo_pointerx()
        y = self.window.winfo_pointery()
        
        tooltip = tk.Toplevel(self.window)
        tooltip.wm_overrideredirect(True)
        tooltip.configure(bg=self.BLUE_GRADIENT_START)
        tooltip.geometry(f"+{x+10}+{y+10}")
        
        # 设置圆角效果和渐变背景
        tooltip.attributes('-alpha', 0.95)
        
        label = ttk.Label(
            tooltip,
            text=text,
            style='Status.TLabel',
            padding=(20, 12)  # 增加提示框内边距
        )
        label.configure(background=self.BLUE_GRADIENT_START, foreground='white')
        label.pack()
        
        # 渐变显示效果
        for i in range(0, 95, 5):
            tooltip.attributes('-alpha', i/100)
            tooltip.update()
            tooltip.after(8)  # 加快动画速度
            
        # 1秒后渐变消失
        def fade_out():
            for i in range(95, 0, -5):
                tooltip.attributes('-alpha', i/100)
                tooltip.update()
                tooltip.after(8)  # 加快动画速度
            tooltip.destroy()
            
        tooltip.after(800, fade_out)
        
    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Navicat配置文件", "*.ncx")]
        )
        if file_path:
            self.file_path_var.set(file_path)
            self.parse_ncx_file(file_path)
            
    def update_status(self, text):
        """更新状态栏文本"""
        self.status_label.configure(text=text)
        
    def parse_ncx_file(self, file_path):
        try:
            # 更新状态
            self.update_status("正在解析文件...")
            
            # 清空现有数据
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # 解析XML文件
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # 检查是否有连接配置
            connections = root.findall(".//Connection")
            if not connections:
                messagebox.showwarning("警告", "当前文件中未找到任何连接配置！")
                self.update_status("就绪")
                return
                
            # 标记是否找到包含密码的连接
            has_password = False
            connection_count = 0
            
            # 遍历所有连接
            for conn in connections:
                conn_name = conn.get("ConnectionName", "")
                host = conn.get("Host", "")
                port = conn.get("Port", "")
                username = conn.get("UserName", "")
                encrypted_password = conn.get("Password", "")
                conn_type = conn.get("ConnType", "")
                
                # 检查是否有密码
                if encrypted_password:
                    has_password = True
                
                # 解密密码
                decrypted_password = NavicatPasswordDecoder.decrypt_password(encrypted_password)
                
                # 添加到表格
                self.tree.insert(
                    "", 
                    tk.END, 
                    values=(
                        conn_name, 
                        host, 
                        port, 
                        username, 
                        encrypted_password,
                        decrypted_password,
                        conn_type
                    )
                )
                connection_count += 1
            
            # 更新状态栏
            self.update_status(f"已加载 {connection_count} 个连接配置")
            
            # 如果没有找到任何包含密码的连接，显示提示
            if not has_password:
                messagebox.showwarning(
                    "警告",
                    "当前连接配置文件中不包含密码信息！\n\n"
                    "请按以下步骤重新导出：\n"
                    "1. 打开 Navicat\n"
                    "2. 选择需要导出的连接\n"
                    "3. 右键点击 -> 导出连接\n"
                    "4. 在导出选项中确保勾选「包含密码」\n"
                    "5. 选择保存位置并导出"
                )
                
        except Exception as e:
            messagebox.showerror("错误", f"解析文件时出错：{str(e)}")
            self.update_status("解析失败")
            
    def on_window_resize(self, event):
        """处理窗口大小改变事件"""
        if event.widget == self.window:
            # 重新计算表格列宽
            self.update_column_widths()
            
    def update_column_widths(self):
        """更新表格列宽"""
        if hasattr(self, 'tree'):
            # 计算可用宽度
            available_width = self.window.winfo_width() - 120  # 预留边距和滚动条空间
            
            # 列宽比例
            column_ratios = {
                "连接名": 0.15,      # 15%
                "主机": 0.15,       # 15%
                "端口": 0.08,       # 8%
                "用户名": 0.12,     # 12%
                "加密密码": 0.20,    # 20%
                "解密密码": 0.18,    # 18%
                "数据库类型": 0.12   # 12%
            }
            
            # 更新每列宽度
            for col, ratio in column_ratios.items():
                width = int(available_width * ratio)
                self.tree.column(col, width=width, minwidth=int(width * 0.8))

    def create_menu(self):
        """创建菜单栏"""
        try:
            print("开始创建菜单...")
            # 创建主菜单栏并保存为实例变量
            self.menubar = tk.Menu(self.window)
            print("主菜单栏创建成功")
            
            # 创建子菜单
            file_menu = tk.Menu(self.menubar, tearoff=0)
            help_menu = tk.Menu(self.menubar, tearoff=0)
            print("子菜单创建成功")
            
            # 添加文件菜单项
            file_menu.add_command(label="打开配置文件", command=self.select_file)
            file_menu.add_separator()
            file_menu.add_command(label="退出", command=self.window.quit)
            print("文件菜单项添加成功")
            
            # 添加帮助菜单项
            help_menu.add_command(label="关于", command=self.show_about)
            print("帮助菜单项添加成功")
            
            # 将子菜单添加到主菜单栏
            self.menubar.add_cascade(label="文件", menu=file_menu)
            self.menubar.add_cascade(label="帮助", menu=help_menu)
            print("子菜单添加到主菜单栏成功")
            
            # 最后设置窗口的菜单栏
            self.window.config(menu=self.menubar)
            print("菜单栏设置到窗口成功")
            
        except Exception as e:
            print(f"创建菜单时出错: {str(e)}")
            print(f"错误类型: {type(e).__name__}")
            print(f"错误详情: {str(e)}")
            # 如果创建菜单失败，继续而不中断程序运行
            pass
            
    def show_about(self):
        """显示关于对话框"""
        about_text = """NaviParser v1.0.0
        
一个用于解析 Navicat 配置文件的工具

作者: xuefei
版权所有 © 2025"""
        
        tk.messagebox.showinfo("关于 NaviParser", about_text)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = NavicatParser()
    app.run() 