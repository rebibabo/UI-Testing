import random
import numpy as np
from cv_digit import recognize_digit
import os
import copy
from PIL import Image
from my_tool import *

def set_seed(seed):
    random.seed(seed)

class Table:
    def __init__(self, table):
        self.width = 10
        self.height = 14
        # self.table = np.array([[random.randint(1, 16) for _ in range(self.width)] for _ in range(self.height)])
        self.table = table
        self.grade = 0  # 记录分数，合成一个的一分
        self.operations = []
        self.max_grade = np.sum(self.table != 0) // 2   # 最大分数

    def load_table(self, str):  # 通过打印出来的表格字符串加载表格
        for i, row in enumerate(str.split('\n')[2:-1]):
            for j in range(5, len(row), 3):
                if row[j:j+2] == '  ':
                    self.table[i][(j-5)//3] = 0
                else:
                    self.table[i][(j-5)//3] = int(row[j:j+2])
        # print(self.show())

    def show(self, merge=None, direction=None, choice=None):    # 显示表格
        str = '       0  1  2  3  4  5  6  7  8  9\n     _______________________________\n'
        str_table = [['' for _ in range(self.width)] for _ in range(self.height)]
        for i, row in enumerate(self.table):
            for j, cell in enumerate(row):
                if cell == 0:   # 空白格子
                    cell = '  '
                else:
                    cell = f'{cell:2}'
                str_table[i][j] = cell
        if merge:   # 如果需要显示合并操作
            x_1, y_1, x_2, y_2 = merge  # (x_1, y_1) 移动到 (x_2, y_2)
            if direction == 0:  # 画向上的箭头
                for i in range(x_2+2, x_1):
                    str_table[i][y_1] = '| '
                str_table[x_2+1][y_1] = '↑ '
            elif direction == 1:    # 画向下的箭头
                for i in range(x_1+1, x_2-1):
                    str_table[i][y_1] = '| '
                str_table[x_2-1][y_1] = '↓ '
            elif direction == 2:    # 画向左的箭头
                for j in range(y_2+2, y_1):
                    str_table[x_1][j] = '--'
                str_table[x_1][y_2+1] = '←-'
            elif direction == 3:    # 画向右的箭头
                for j in range(y_1+1, y_2-1):
                    str_table[x_1][j] = '--'
                str_table[x_1][y_2-1] = '-→'
            if x_1 == x_2:  # 如果是同一列，没有箭头可以画，用：连接
                for i in range(min(x_2, choice[0])+1, max(x_2, choice[0])):
                    str_table[i][y_2] = '：'
            if y_1 == y_2:  # 如果是同一行，没有箭头可以画，用··连接
                for i in range(min(y_2, choice[1])+1, max(y_2, choice[1])):
                    str_table[x_2][i] = '··'
            str_table[x_1][y_1] = '▢ '  # 移动的初始格子变成▢
            str_table[x_2][y_2] = '▢ '  # 移动后消除的目标格子
            str_table[choice[0]][choice[1]] = '▢ '  # 移动后的格子
        for i, row in enumerate(self.table):    # 打印行列号
            str += f'{i:<4}｜'
            for j, cell in enumerate(row):
                str += f'{str_table[i][j]} '
            str = str[:-1] + '｜\n'
        str += '     ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾'
        return str

    def find_adj(self, x, y, direction):    # 找到连续空白格子对面第一个非空白的格子，方向用direction表示
        if direction == 0:
            for i in range(x-1, -1, -1):
                if self.table[i][y] != 0 or i == 0:  # 遇到非空白格子或边界
                    return i, y
        elif direction == 1:
            for i in range(x+1, self.height):
                if self.table[i][y] != 0 or i == self.height - 1:
                    return i, y
        elif direction == 2:
            for j in range(y-1, -1, -1):
                if self.table[x][j] != 0 or j == 0:
                    return x, j
        elif direction == 3:
            for j in range(y+1, self.width):
                if self.table[x][j] != 0 or j == self.width - 1:
                    return x, j
        return x, y

    def find_margin(self, x, y, direction): # 找到连续非空白格子的边界，方向用direction表示
        if direction == 0:
            for i in range(x, -1, -1):
                if i == 0 or self.table[i-1][y] == 0:   # 遇到空白格子或边界
                    return i, y
        elif direction == 1:
            for i in range(x, self.height):
                if i == self.height- 1 or self.table[i+1][y] == 0:
                    return i, y
        elif direction == 2:
            for j in range(y, -1, -1):
                if j == 0 or self.table[x][j-1] == 0:
                    return x, j
        elif direction == 3:
            for j in range(y, self.width):
                if j == self.width - 1 or self.table[x][j+1] == 0:
                    return x, j

    def equal(self, coord1, coord2):    # 判断两个坐标是否不同且对应的图像相同
        return coord1 != coord2 and self.table[coord1[0]][coord1[1]] == self.table[coord2[0]][coord2[1]]

    def move(self, x_1, x_2, y_1, y_2, direction):  # 移动格子，将x_1, y_1移动到x_2, y_2，方向用direction表示
        if direction == -1: 
            return
        margin = self.find_margin(x_1, y_1, direction)  # 找到x_1, y_1沿direction方向的边界
        if direction == 0:
            self.table[x_2-x_1+margin[0]:x_2+1, y_1] = self.table[margin[0]:x_1+1, y_1] # 将这部分整体往上移动到x_2
            self.table[max(margin[0], x_2+1):x_1+1, y_1] = 0    # 将原始位置元素清0
        elif direction == 1:
            self.table[x_2:x_2+margin[0]-x_1+1, y_1] = self.table[x_1:margin[0]+1, y_1] # 将这部分整体往下移动到x_2
            self.table[x_1:min(x_2, margin[0]+1), y_1] = 0
        elif direction == 2:
            self.table[x_1, y_2-y_1+margin[1]:y_2+1] = self.table[x_1, margin[1]:y_1+1] # 将这部分整体往左移动到y_2
            self.table[x_1, max(margin[1], y_2+1):y_1+1] = 0
        elif direction == 3:
            self.table[x_1, y_2:y_2+margin[1]-y_1+1] = self.table[x_1, y_1:margin[1]+1] # 将这部分整体往右移动到y_2
            self.table[x_1, y_1:min(y_2, margin[1]+1)] = 0

    def merge(self, x_1, y_1, x_2, y_2, stop=False):    # 合并操作，首先判断是否可以合并，然后移动，最后消除
        '''↑:0 ↓:1 ←:2 →:3'''
        if self.table[x_1, y_1] == 0:   # 空白格子不能移动
            return
        if x_1 == x_2 and y_1 == y_2:   # 不能合并相同的格子
            direction = -1
        elif x_1 == x_2:    # 同一行可以移动
            direction = 2 + int(y_1 < y_2)
        elif y_1 == y_2:    # 同一列可以移动
            direction = int(x_1 < x_2)
        else:   # 不能移动
            return
        if direction in [0, 1]:
            margin = self.find_margin(x_1, y_1, direction)  # 找到x_1, y_1沿direction方向的边界
            adjac = self.find_adj(margin[0], margin[1], direction)  # 从边界沿direction方向找到第一个非空白格子
            length = abs(margin[0] - adjac[0])  # 计算连续空白格子的长度
            if abs(x_2 - x_1) >= length:    # 如果连续非空白格子长度超过了空白区域的长度，不能移动
                return
        elif direction in [2, 3]:
            margin = self.find_margin(x_1, y_1, direction)
            adjac = self.find_adj(margin[0], margin[1], direction)
            length = abs(margin[1] - adjac[1])
            if abs(y_2 - y_1) >= length:
                return
        table = copy.deepcopy(self.table)   # 先暂时保存原表格
        self.move(x_1, x_2, y_1, y_2, direction)    # 移动
        left = self.find_adj(x_2, y_2, 2)   # 找到移动后左边第一个非空白格子
        right = self.find_adj(x_2, y_2, 3)  # 找到移动后右边第一个非空白格子
        up = self.find_adj(x_2, y_2, 0)     # 找到移动后上边第一个非空白格子
        down = self.find_adj(x_2, y_2, 1)   # 找到移动后下边第一个非空白格子
        choices = []    # 记录上下左右可以消除的格子
        if self.equal(up, (x_2, y_2)) and direction in [-1, 2, 3]:
            choices.append(up)
        if self.equal(down, (x_2, y_2)) and direction in [-1, 2, 3]:
            choices.append(down)
        if self.equal(left, (x_2, y_2)) and direction in [-1, 0, 1]:
            choices.append(left)
        if self.equal(right, (x_2, y_2)) and direction in [-1, 0, 1]:
            choices.append(right)
        if len(choices) == 0 or len(choices) > 1:   # 没有可以消除的格子，也限制有多个选择的情况
            self.table = table  # 恢复原表格
            return
        choice = choices[0] 
        self.operations.append((x_1, y_1, x_2, y_2))    # 记录操作
        self.grade += 1 # 分数+1
        self.table[x_2, y_2] = 0    # 将目标格子消除
        self.table[choice[0], choice[1]] = 0    # 将匹配的格子消除
        if stop:    # 如果stop为True，打印出操作过程
            direction_dict = {-1: '.', 0: '↑', 1: '↓', 2: '←', 3: '→'}
            print(f'current grade: {self.grade}, step: {(x_1, y_1, x_2, y_2)}, direction: {direction_dict[direction]}')
            input(self.show((x_1, y_1, x_2, y_2), direction, choice))
            
def run(table: Table, N=400000, stop=False): # 运行一次程序
    # input(table.show())
    for _ in range(N): # 随机尝试N次
        x_1 = random.randint(0, table.height- 1)
        y_1 = random.randint(0, table.width - 1)
        x_2 = random.randint(0, table.height- 1)
        y_2 = random.randint(0, table.width - 1)
        table.merge(x_1, y_1, x_2, y_2, stop)
    # print(table.show())
    return table    # 返回表格，用于获取最终得分

if __name__ == '__main__':
    max_grade = 0
    best_seed = 0
    for file in os.listdir('.'):
        if file.endswith('.jpg'):
            t = np.array(recognize_digit(file))
            break
    for i in range(14, 200):    # 设置随机种子，然后在随机种子中获取满分操作
        set_seed(i)
        t_copy = copy.deepcopy(t)
        table = Table(t_copy)
        table = run(table)
        print(f'seed: {i}, grade: {table.grade}, best seed: {best_seed}, max grade: {max_grade}, therotic max grade: {table.max_grade}')
        if table.grade > max_grade:
            max_grade = table.grade
            best_seed = i
            if table.grade >= table.max_grade - 1:  # 如果达到理论最高分，或者最高分少一，则一定可以消除完
                break

    set_seed(best_seed)
    table = Table(t)
    table = run(table, stop=False)
    with open('output.txt', 'w') as f:
        for each in table.operations:
            f.write(f'{each[0]} {each[1]} {each[2]} {each[3]}\n')
