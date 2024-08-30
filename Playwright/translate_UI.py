import tkinter as tk
from tkinter import messagebox
from playwright.sync_api import sync_playwright
import re

# 全局变量声明
playwright = None
browser = None
context = None
page = None

# 初始化Playwright和页面
def initialize_playwright():
    global playwright, browser, context, page
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://fanyi.youdao.com/#/")
    page.locator(".close").click()
    page.locator("div").filter(has_text=re.compile(r"^翻译$")).click()
    page.locator(".ic_language_arrowdown").first.click()
    page.get_by_text("英语").first.click()
    page.wait_for_timeout(1000)

# 定义翻译函数
def translate_text():
    input_text = input_box.get("1.0", "end-1c").strip().replace('\n', ' ')
    if not input_text:
        messagebox.showwarning("输入错误", "请输入要翻译的文本")
        return

    page.locator("#js_fanyi_input").click()
    page.locator("#js_fanyi_input").fill(input_text)
    page.wait_for_timeout(1000)

    if page.locator(".pron").count():
        results = []
        for text in page.locator(".pron").all_inner_texts():
            split = text.split()
            if not split:
                continue
            else:
                results.append(f"{split[0]}: /{split[1]}/")
        results.append(page.locator(".paraphrase-container").first.inner_text())
        translation_result = "\n".join(results)
    else:
        translation_result = page.locator(".tgt.un-step-trans").inner_text()

    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, translation_result)
    output_box.config(state=tk.DISABLED)

# 清空输入和输出框
def clear_text():
    input_box.delete("1.0", tk.END)
    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    output_box.config(state=tk.DISABLED)

# 创建主窗口
root = tk.Tk()
root.title("翻译工具")

# 创建并放置输入框、按钮和输出框
input_box = tk.Text(root, height=10, width=50, font=("Times New Roman", 14))
input_box.pack(pady=10)

translate_button = tk.Button(root, text="翻译", command=translate_text, font=("楷体", 14))
translate_button.pack(pady=5)

# 使用楷体字体显示输出
clear_button = tk.Button(root, text="清空", command=clear_text, font=("楷体", 14))
clear_button.pack(pady=5)

output_box = tk.Text(root, height=10, width=50, state=tk.DISABLED, font=("楷体", 14))
output_box.pack(pady=10)

# 初始化Playwright
initialize_playwright()

# 运行主循环
root.mainloop()

# 关闭Playwright
def close_playwright():
    global playwright, browser, context
    if context:
        context.close()
    if browser:
        browser.close()
    if playwright:
        playwright.stop()

root.protocol("WM_DELETE_WINDOW", lambda: [close_playwright(), root.destroy()])


