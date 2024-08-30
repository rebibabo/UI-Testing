from uiautomation import WindowControl
import time
import os
import pyautogui
import pyperclip
pyautogui.FAILSAFE = False

wx = WindowControl(Name='微信')
wx.SwitchToThisWindow()
wx.ListItemControl(Name='文件传输助手').Click()

def send_file(file_path):
    wx.ButtonControl(Name='发送文件').Click()   # 点击发送文件按钮
    select = WindowControl(Name='打开')         # 选择文件窗口
    select.SwitchToThisWindow()
    select.EditControl(Name='文件名(N):').SendKeys(file_path)   # 输入文件路径
    select.SplitButtonControl(Name='打开(O)').Click()
    send = WindowControl(Name='DragAttachWnd')  # 发送文件窗口
    send.ButtonControl(Name="发送（1）").Click()    # 点击发送按钮

def send_msg(msg):
    editor = wx.EditControl(Name='文件传输助手')
    editor.Click()
    pyperclip.copy(msg)
    pyautogui.hotkey('ctrl', 'v') # 使用快捷键复制粘贴，不然太慢而且换行有问题
    editor.SendKeys('{ENTER}')

while True:
    time.sleep(1)
    msg_list = wx.ListControl(Name="消息")
    last_msg = msg_list.GetChildren()[-1].Name
    if last_msg.startswith('ls'):
        path = last_msg.split('ls ')[1]
        if path.startswith('/'):
            path = 'C:\\Users\\28413\\Desktop\\' + path[1:].replace('/', '\\')
        if not os.path.exists(path):
            send_msg('路径不存在')
            continue
        send_msg('\n'.join(os.listdir(path)))
    elif last_msg.startswith('send'):
        path = last_msg.split('send ')[1]
        if path.startswith('/'):
            path = 'C:\\Users\\28413\\Desktop\\' + path[1:].replace('/', '\\')
        if not os.path.exists(path):
            send_msg('文件不存在')
            continue
        send_file(path)