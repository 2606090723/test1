import tkinter as tk
from PIL import Image, ImageTk
import random, os, threading, time

class DesktopPet:
    def __init__(self, root, img_files, talk_file=None):
        self.root = root
        self.root.overrideredirect(True)  # 无边框
        self.root.wm_attributes('-topmost', True)
        self.root.wm_attributes('-transparentcolor', 'white')

        # 加载动画帧
        self.imgs = [ImageTk.PhotoImage(Image.open(f)) for f in img_files]
        self.img_idx = 0

        self.pet_label = tk.Label(root, image=self.imgs[self.img_idx], bg='white')
        self.pet_label.pack()

        # 初始位置
        self.x, self.y = 300, 300
        self.root.geometry(f'+{self.x}+{self.y}')

        # 拖动
        self.pet_label.bind("<ButtonPress-1>", self.start_move)
        self.pet_label.bind("<B1-Motion>", self.do_move)

        # 右键菜单
        self.pet_label.bind("<Button-3>", self.show_menu)
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="说句话", command=self.say_something)
        self.menu.add_command(label="跟随鼠标5秒", command=self.follow_mouse)
        self.menu.add_separator()
        self.menu.add_command(label="隐藏", command=self.hide)
        self.menu.add_command(label="显示", command=self.show)
        self.menu.add_separator()
        self.menu.add_command(label="退出", command=self.root.destroy)

        # 说话气泡
        self.bubble = None
        self.talk_lines = []
        if talk_file and os.path.exists(talk_file):
            with open(talk_file, encoding='utf-8') as f:
                self.talk_lines = [line.strip() for line in f if line.strip()]

        # 动画循环
        self.animate()
        self.move_pet()
        self.auto_talk()

    # 拖动
    def start_move(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def do_move(self, event):
        x = self.root.winfo_pointerx() - self.offset_x
        y = self.root.winfo_pointery() - self.offset_y
        self.x, self.y = x, y
        self.root.geometry(f'+{self.x}+{self.y}')

    # 动画
    def animate(self):
        self.img_idx = (self.img_idx + 1) % len(self.imgs)
        self.pet_label.config(image=self.imgs[self.img_idx])
        self.root.after(300, self.animate)

    # 自由移动
    def move_pet(self):
        dx, dy = random.randint(-10, 10), random.randint(-10, 10)
        self.x += dx
        self.y += dy
        self.root.geometry(f'+{self.x}+{self.y}')
        self.root.after(2000, self.move_pet)

    # 右键菜单
    def show_menu(self, event):
        self.menu.tk_popup(event.x_root, event.y_root)

    # 隐藏/显示
    def hide(self):
        self.root.withdraw()
    def show(self):
        self.root.deiconify()

    # 说话
    def say_something(self, text=None):
        if not text:
            text = random.choice(self.talk_lines) if self.talk_lines else "你好呀！"
        if self.bubble:
            self.bubble.destroy()
        self.bubble = tk.Toplevel(self.root)
        self.bubble.overrideredirect(True)
        self.bubble.wm_attributes('-topmost', True)
        self.bubble.geometry(f'+{self.x+60}+{self.y-30}')
        tk.Label(self.bubble, text=text, bg='lightyellow', font=('微软雅黑', 12)).pack()
        self.bubble.after(2000, self.bubble.destroy)

    def auto_talk(self):
        self.say_something()
        self.root.after(random.randint(5000, 12000), self.auto_talk)

    # 跟随鼠标
    def follow_mouse(self):
        def follow():
            end_time = time.time() + 5
            while time.time() < end_time:
                mx = self.root.winfo_pointerx() - 50
                my = self.root.winfo_pointery() - 50
                self.x, self.y = mx, my
                self.root.geometry(f'+{mx}+{my}')
                time.sleep(0.03)
        threading.Thread(target=follow, daemon=True).start()

if __name__ == "__main__":
    # 多帧图片，如 pet1.png, pet2.png, pet3.png...
    imgs = [f"pet{i}.png" for i in range(1, 4) if os.path.exists(f"pet{i}.png")]
    if not imgs:
        print("请准备多帧宠物图片 pet1.png, pet2.png, ...")
        exit()
    root = tk.Tk()
    pet = DesktopPet(root, imgs, "pet_words.txt")
    root.mainloop()
