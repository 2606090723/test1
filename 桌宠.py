import tkinter as tk
import random
import sys

class DesktopPet:
    def __init__(self):
        # --- 窗口设置 ---
        self.window = tk.Tk()
        # 隐藏标题栏和边框
        self.window.overrideredirect(True)
        # 设置窗口置顶
        self.window.wm_attributes("-topmost", True)
        
        # --- 宠物图片 ---
        try:
            # 加载 PNG 图片
            self.pet_image = tk.PhotoImage(file='a.png')
        except tk.TclError:
            print("错误：无法加载 'pet.png'。请确保文件存在且为PNG格式。")
            sys.exit()

        # 设置窗口透明颜色（例如，白色）。这需要你的PNG图片背景是纯色的。
        # 如果你的PNG是真正透明的，Tkinter可能无法完美处理，但通常对于简单背景有效。
        # 我们将Label的背景设置为一个不太可能出现在宠物身上的颜色，比如'snow'
        transparent_color = 'snow' 
        self.window.wm_attributes("-transparentcolor", transparent_color)
        
        self.image_label = tk.Label(self.window, image=self.pet_image, bd=0, bg=transparent_color)
        self.image_label.pack()

        # --- 宠物状态 ---
        self.x_offset = 0
        self.y_offset = 0
        
        # --- 绑定事件 ---
        # 鼠标左键按下事件，用于开始拖动
        self.image_label.bind("<ButtonPress-1>", self.start_drag)
        # 鼠标左键拖动事件
        self.image_label.bind("<B1-Motion>", self.do_drag)
        # 添加右键菜单来退出程序
        self.image_label.bind("<Button-3>", self.show_menu)
        
        # --- 获取屏幕尺寸 ---
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        
        # 随机设置初始位置
        start_x = random.randint(0, self.screen_width - self.pet_image.width())
        start_y = random.randint(0, self.screen_height - self.pet_image.height())
        self.window.geometry(f"+{start_x}+{start_y}")
        
        # --- 启动循环 ---
        self.random_move()
        
        # 启动Tkinter主循环
        self.window.mainloop()

    def start_drag(self, event):
        """记录鼠标按下时的位置"""
        self.x_offset = event.x
        self.y_offset = event.y

    def do_drag(self, event):
        """根据鼠标移动更新窗口位置"""
        new_x = self.window.winfo_pointerx() - self.x_offset
        new_y = self.window.winfo_pointery() - self.y_offset
        self.window.geometry(f"+{new_x}+{new_y}")

    def random_move(self):
        """随机移动宠物"""
        current_x = self.window.winfo_x()
        current_y = self.window.winfo_y()
        
        # 随机生成一个移动目标点
        move_x = random.randint(-30, 30)
        move_y = random.randint(-30, 30)
        
        new_x = current_x + move_x
        new_y = current_y + move_y
        
        # 确保宠物不会移出屏幕
        pet_width = self.pet_image.width()
        pet_height = self.pet_image.height()
        
        if new_x < 0:
            new_x = 0
        if new_x > self.screen_width - pet_width:
            new_x = self.screen_width - pet_width
        
        if new_y < 0:
            new_y = 0
        if new_y > self.screen_height - pet_height:
            new_y = self.screen_height - pet_height
            
        self.window.geometry(f"+{new_x}+{new_y}")
        
        # 每隔3秒随机移动一次
        self.window.after(3000, self.random_move)
        
    def show_menu(self, event):
        """显示右键菜单"""
        menu = tk.Menu(self.window, tearoff=0)
        menu.add_command(label="退出", command=self.window.destroy)
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

# --- 主程序入口 ---
if __name__ == "__main__":
    DesktopPet()
