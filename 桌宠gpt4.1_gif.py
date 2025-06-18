import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

class GifPet:
    def __init__(self, root, gif_file):
        self.root = root
        self.root.overrideredirect(True)  # 无边框
        self.root.wm_attributes('-topmost', True)
        self.root.wm_attributes('-transparentcolor', 'white')

        # 加载gif所有帧
        self.img = Image.open(gif_file)
        self.frames = [ImageTk.PhotoImage(frame.convert("RGBA")) for frame in ImageSequence.Iterator(self.img)]
        self.idx = 0

        self.pet_label = tk.Label(root, image=self.frames[0], bg='white')
        self.pet_label.pack()

        # 初始位置
        self.x, self.y = 300, 300
        self.root.geometry(f'+{self.x}+{self.y}')

        # 拖动事件
        self.pet_label.bind("<ButtonPress-1>", self.start_move)
        self.pet_label.bind("<B1-Motion>", self.do_move)

        self.animate()

    def start_move(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def do_move(self, event):
        x = self.root.winfo_pointerx() - self.offset_x
        y = self.root.winfo_pointery() - self.offset_y
        self.x, self.y = x, y
        self.root.geometry(f'+{self.x}+{self.y}')

    def animate(self):
        self.idx = (self.idx + 1) % len(self.frames)
        self.pet_label.config(image=self.frames[self.idx])
        self.root.after(100, self.animate)  # 根据你的gif帧数和速度调整

if __name__ == "__main__":
    root = tk.Tk()
    pet = GifPet(root, "c0f8-ihmipqx0162353.gif")
    root.mainloop()
