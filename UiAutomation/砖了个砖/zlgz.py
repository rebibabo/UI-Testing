from uiautomation import WindowControl, PaneControl
from MCTS import MCTS, TreeNode
from Table import NewTable
import time
from copy import deepcopy
import os

while True:     # 循环打关卡
    if os.path.exists('screenshot.jpg'):
        os.remove('screenshot.jpg')

    vscode = PaneControl(Name='zlgz.py - 砖了个砖 - Visual Studio Code [Administrator]')    # 打开vscode
    vscode.SwitchToThisWindow()
    vscode.TreeItemControl(Name='screenshot.js').Click()    # 运行截图脚本，将截图保存发送给微信的文件传输助手
    vscode.ButtonControl(Name='运行脚本(Run) (F5)').Click()
    vscode.TreeItemControl(Name='zlgz.py').Click()  # 回到主脚本
    time.sleep(12)

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

    iters = 10
    child_iters = 10
    total_grade = 0
    for i in range(iters):
        grade = 0
        operations = []
        table = NewTable(load_from_pic=True)
        ori_table = deepcopy(table)
        new_table = deepcopy(table)
        root = TreeNode(new_table, None, None)
        root_copy = deepcopy(root)
        max_grade = table.max_grade
        print(f"Iteration {i+1}/{iters}")
        while not table.done:
            root = MCTS(root, child_iters)
            table.step(*root.action)
            operations.append(list(root.action))
            grade += 1
            print(f"iter {i+1}: {grade}")
        child_iters += 5
        if grade == max_grade or i == iters-1:
            with open("result.txt", "w") as f:
                for op in operations:
                    if op[4] == 4:
                        op[2], op[3] = op[0], op[1]
                    elif op[4] in [2, 3]:
                        op[2] = op[0]
                    else:
                        op[3] = op[1]
                    f.write(f"{op[0]} {op[1]} {op[2]} {op[3]}\n")
            break

    def map(x, y):
        return int(y*55.4) + 47, int(x*54.8) + 312

    win = WindowControl(Name='23127PN0CC')  # 打开scrcpy软件的手机投屏
    win.SwitchToThisWindow()

    with open("result.txt", "r") as f:
        grade = 0
        for line in f:
            grade += 1
            x_1, y_1, x_2, y_2 = [int(i) for i in line.strip().split()]
            x_1, y_1 = map(x_1, y_1)
            x_2, y_2 = map(x_2, y_2)
            win.MoveCursorToInnerPos(x_1, y_1)  # 移动鼠标到起始位置
            time.sleep(0.3)
            if x_1 == x_2 and y_1 == y_2:
                win.Click(x_1, y_1) # 如果不需要移动，直接点击
            else:
                win.DragDrop(x_1, y_1, x_2, y_2, moveSpeed=0.5) # 移动鼠标到终止位置
        if table.grade < table.max_grade:  # 没有找到解，点击看视频按钮，刷新
            time.sleep(1)
            win.Click(300, 1225)
            time.sleep(32)
            win.Click(550, 90)
    time.sleep(6)