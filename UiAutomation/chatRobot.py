from uiautomation import WindowControl
import time
import pyautogui
import pyperclip
from playwright.sync_api import Playwright, sync_playwright, expect
import time

def print_response(page, index):
    length = 0
    while not page.locator(f"[data-index='{index}'] .markdown___vuBDJ").count():    # 等待加载回答框
        time.sleep(0.01)
    lc = page.locator(f"[data-index='{index}'] .markdown___vuBDJ").last  # 定位回答信息，忽略停止生成、正在搜索、再试一次等信息
    while not page.locator('[data-testid="msh-chat-segment-reAnswer"]').count():    # 当没有出现再试一次时，说明回答还不完整
        new_length = len(lc.inner_text())  # 获取回答信息的长度
        print(lc.inner_text()[length:new_length], end='')  # 打印新增的回答信息
        length = new_length
        time.sleep(0.01)
    page.wait_for_timeout(500)
    # print(lc.inner_text()[length:]) # 打印最后的回答信息
    return lc.inner_text()

user = '文件传输助手'
wx = WindowControl(Name='微信')
wx.SwitchToThisWindow()
wx.ListItemControl(Name=user).Click()

def send_msg(msg):
    editor = wx.EditControl(Name=user)
    editor.Click()
    pyperclip.copy(msg)
    pyautogui.hotkey('ctrl', 'v') # 使用快捷键复制粘贴，不然太慢而且换行有问题
    editor.SendKeys('{ENTER}')

def get_msg_list():
    msg_list = wx.ListControl(Name="消息")
    return msg_list.GetChildren()[-1].Name

with sync_playwright() as playwright:
    send_msg("在吗？")
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://kimi.moonshot.cn/")
    page.locator(".css-1mdh3j9").click()    # 点击登录
    page.locator("#phone").fill("19891771663")  # 输入手机号
    page.wait_for_timeout(2000)  # 等待加载
    page.locator("[data-testid='send-verify-code']").click()   # 发送验证码
    input("Please input the captcha manually, after you finish, please enter any key to continue...")
    page.wait_for_timeout(500)  # 等待加载
    page.get_by_role("paragraph").click()
    page.get_by_test_id("msh-chatinput-editor").fill("请你假设你是我的朋友，我想和你一起聊天，你的回答“不要”超过20个字，你先问我“在吗”，“只”问“在吗”")
    page.get_by_test_id("msh-chatinput-send-button").click()
    data_index = 2
    previous_msg = get_msg_list()
    reply = ''
    while True:
        time.sleep(5)
        current_msg = get_msg_list()
        if current_msg != previous_msg and current_msg != reply:
            previous_msg = current_msg
            data_index += 2
            page.get_by_test_id("msh-chatinput-editor").fill(current_msg)
            page.get_by_test_id("msh-chatinput-send-button").click()
            reply = print_response(page, data_index)
            send_msg(reply)