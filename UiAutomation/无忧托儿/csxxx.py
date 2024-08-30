from uiautomation import WindowControl, PaneControl
from game import *
import time
import os

first = True

while True:
    win = WindowControl(Name='23127PN0CC')  # 打开scrcpy软件的手机投屏
    win.SwitchToThisWindow()

    if os.path.exists('screenshot.jpg'):
        os.remove('screenshot.jpg')

    vscode = PaneControl(Name='csxxx.py - 无忧托儿 - Visual Studio Code [Administrator]')    # 打开vscode
    vscode.SwitchToThisWindow()
    vscode.TreeItemControl(Name='screenshot.js').Click()    # 运行截图脚本，将截图保存发送给微信的文件传输助手
    win.Click(200, 600)
    vscode.ButtonControl(Name='运行脚本(Run) (F5)').Click()
    vscode.TreeItemControl(Name='csxxx.py').Click()  # 回到主脚本
    time.sleep(8)

    wx = WindowControl(Name='微信') # 打开微信，将截图保存到当前文件夹
    wx.SwitchToThisWindow()
    wx.ListItemControl(Name='文件传输助手').Click()
    msg_list = wx.ListControl(Name="消息")
    last_msg = msg_list.GetChildren()[-1]
    last_msg.GetChildren()[0].GetChildren()[1].Click()
    new_win = WindowControl(Name="图片查看")
    time.sleep(2)
    new_win.ButtonControl(Name="另存为...").Click()
    save_win = WindowControl(Name="另存为...")
    save_win.EditControl(Name="文件名:").SendKeys(f"{os.getcwd()}\\screenshot.jpg")
    save_win.ButtonControl(Name="保存(S)").Click()
    new_win.ButtonControl(Name="关闭").Click()
    wx.Minimize()

    max_grade = 0
    best_seed = 0
    if first:
        iter = 50
        first = False
    else:
        iter = 3
    for i in range(iter):
        set_seed(i)
        grade = run().grade
        print(f'seed: {i}, grade: {grade}, max_grade: {max_grade}, best_seed: {best_seed}')
        if grade > max_grade:
            max_grade = grade
            best_seed = i

    set_seed(best_seed)
    table = run(stop=False)

    with open("result.txt", "w") as f:  # 保存操作序列到文件
        for x_1, y_1, x_2, y_2 in table.operations:
            f.write(f"{x_1} {y_1} {x_2} {y_2}\n")

    def map(x, y):
        return int(y*52 + 61), int(x*52 + 336)

    win.SwitchToThisWindow()
    win.Click(500, 600)

    with open("result.txt", "r") as f:
        for line in f:
            x_1, y_1, x_2, y_2 = [int(i) for i in line.strip().split()]
            x_1, y_1 = map(x_1, y_1)
            x_2, y_2 = map(x_2, y_2)
            win.MoveCursorToInnerPos(x_1, y_1)  # 移动鼠标到起始位置
            time.sleep(0.05)
            win.DragDrop(x_1, y_1, x_2, y_2, moveSpeed=5) # 移动鼠标到终止位置

    win.MoveCursorToInnerPos(300, 1300)
    win.DragDrop(300, 1300, 300, 1000, moveSpeed=5)
    win.MoveCursorToInnerPos(300, 1315)
    win.DragDrop(300, 1315, 300, 1000, moveSpeed=20)