import tkinter as tk
from docx import Document
import random

# 全局变量
title_list = []
content_dict = {}
current_title_index = -1

# 提取标题和内容
def extract_title_and_content(doc):
    global title_list, content_dict
    title_list = []
    content_dict = {}

    paragraphs = doc.paragraphs
    is_title = False
    title = ""
    content = []

    for para in paragraphs:
        if para.text.strip().startswith("2") and is_english(para.text):
            if is_title:
                content_dict[title] = content
            title = para.text
            content = []
            is_title = True
        elif is_title:
            if para.text.strip() != "":
                content.append(para.text)
            if para.text.strip() == "" or para == paragraphs[-1]:
                content_dict[title] = content
                is_title = False

    title_list = list(content_dict.keys())

# 判断英文文本
def is_english(text):
    return all(ord(char) < 128 for char in text)

# 更新标题
def update_title():
    global current_title_index
    current_title_index = random.randint(0, len(title_list) - 1)
    title_label.config(text=title_list[current_title_index], font=("Helvetica", 16, "bold"))

# 显示内容
def show_content():
    update_title()
    countdown(1, "blue")  # 1秒蓝色倒计时

def start_15_second_countdown():
    countdown(15, "black")  # 15秒黑色倒计时
    time_label.after(15000, start_45_second_countdown)  # 在15秒后启动45秒倒计时

def start_45_second_countdown():
    countdown(45, "black")  # 45秒黑色倒计时
    time_label.after(45000, show_full_content)  # 在45秒后显示完整内容

# 倒计时
def countdown(seconds, color="black"):
    if seconds > 0:
        time_label.config(text=seconds, fg=color)
        time_label.after(1000, countdown, seconds - 1, color)
    else:
        time_label.config(text="完成")

# 显示完整内容
def show_full_content():
    content = "\n".join(content_dict[title_list[current_title_index]])
    content_text.delete("1.0", tk.END)
    content_text.insert(tk.END, content)

# 其他函数定义
def reset_page():
    title_label.config(text="")
    content_text.delete("1.0", tk.END)
    update_title()
    time_label.after(1000, start_15_second_countdown)  # 在1秒后启动15秒倒计时

# 主程序
doc = Document(r"C:\Users\ICE\Downloads\Task1.docx")

window = tk.Tk()
window.title("托福口语模拟答题")

title_label = tk.Label(window, wraplength=500, font=("Helvetica", 16, "bold"))
content_text = tk.Text(window, wrap=tk.WORD, font=("Helvetica", 12))
time_label = tk.Label(window, font=("Helvetica", 18))

start_btn = tk.Button(window, text="Start", command=reset_page, font=("Helvetica", 14))  # 添加开始按钮

time_label.pack()
title_label.pack()
content_text.pack(fill=tk.BOTH, expand=True, pady=20)
start_btn.pack(side="bottom", pady=10)  # 放在下方

extract_title_and_content(doc)

window.mainloop()
