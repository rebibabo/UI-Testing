from cv_digit import recognize_digit
import numpy as np
import os

class NewTable:
    width = 10
    height = 14
    grade = 0
    operations = []
    done: bool = None
    _actions: list[int] = None
    taken_step: bool = False

    def __init__(self, 
        load_from_pic: bool = False,
        table_str: str = '', 
    ):
        if load_from_pic:
            files = os.listdir('./')
            for file in files:
                if file.endswith('.jpg'):
                    self.table = np.array(recognize_digit(file))
                    break
        elif table_str:
            self.load_table(table_str)
        else:
            table_str = open("table.txt", "r", encoding='utf-8').read()
            self.load_table(table_str)
        self.solutions = []

    def load_table(self, str):
        self.table = np.zeros((self.height, self.width), dtype=int)
        for i, row in enumerate(str.split('\n')[2:-1]):
            for j in range(5, len(row), 3):
                if row[j:j+2] == '  ':
                    self.table[i][(j-5)//3] = 0
                else:
                    self.table[i][(j-5)//3] = int(row[j:j+2])

    def show(self, step=None, direction=None, choice=None):
        str = '       0  1  2  3  4  5  6  7  8  9\n     _______________________________\n'
        str_table = [['' for _ in range(self.width)] for _ in range(self.height)]
        for i, row in enumerate(self.table):
            for j, cell in enumerate(row):
                if cell == 0:
                    cell = '  '
                else:
                    cell = f'{cell:2}'
                str_table[i][j] = cell
        if step:
            x_1, y_1, x_2, y_2 = step
            if direction == 0:
                for i in range(x_2+2, x_1):
                    str_table[i][y_1] = '| '
                str_table[x_2+1][y_1] = '↑ '
            elif direction == 1:
                for i in range(x_1+1, x_2-1):
                    str_table[i][y_1] = '| '
                str_table[x_2-1][y_1] = '↓ '
            elif direction == 2:
                for j in range(y_2+2, y_1):
                    str_table[x_1][j] = '--'
                str_table[x_1][y_2+1] = '←-'
            elif direction == 3:
                for j in range(y_1+1, y_2-1):
                    str_table[x_1][j] = '--'
                str_table[x_1][y_2-1] = '-→'
            if x_1 == x_2:
                for i in range(min(x_2, choice[0])+1, max(x_2, choice[0])):
                    str_table[i][y_2] = '：'
            if y_1 == y_2:
                for i in range(min(y_2, choice[1])+1, max(y_2, choice[1])):
                    str_table[x_2][i] = '··'
            str_table[x_1][y_1] = '▢ '
            str_table[x_2][y_2] = '▢ '
            str_table[choice[0]][choice[1]] = '▢ '
        for i, row in enumerate(self.table):
            str += f'{i:<4}｜'
            for j, cell in enumerate(row):
                str += f'{str_table[i][j]} '
            str = str[:-1] + '｜\n'
        str += '     ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾'
        print(str)

    @ property
    def max_grade(self):
        return np.sum(self.table != 0) // 2
        
    @ property
    def done(self):
        if self._actions is not None and not self.taken_step:
            return len(self._actions) == 0
        else:
            self._actions = self.action_space()
            self.taken_step = False
            return len(self._actions) == 0

    @ property
    def actions(self):
        if self._actions is None or self.taken_step:
            self._actions = self.action_space()
        self.taken_step = False
        return self._actions

    def action_space(self):
        solutions = []
        for i in range(self.height * self.width):
            x, y = i // self.width, i % self.width
            ele = self.table[x][y]
            if ele == 0:
                continue
            for j in range(i + 1, self.height * self.width):
                x2, y2 = j // self.width, j % self.width
                ele2 = self.table[x2][y2]
                if ele2 == 0:
                    continue
                if ele == ele2:
                    d1 = self.test(x, y, x2, y2)
                    for d in d1:
                        solutions.append((x, y, x2, y2, d))
                    d2 = self.test(x2, y2, x, y)
                    if (x, y) == (2, 8) and (x2, y2) == (3, 6):
                        self.test(x2, y2, x, y)
                    for d in d2:
                        if d != 4:
                            solutions.append((x2, y2, x, y, d))
        return solutions

    def test_line(self, x, y, x2, y2, type):
        if type == 0:   # ----
            a, b = min(y, y2), max(y, y2)
            for i in range(a + 1, b):
                if self.table[x2][i] != 0:
                    return False
            return True 
        else:   # |
            a, b = min(x, x2), max(x, x2)
            for i in range(a + 1, b):
                if self.table[i][y2] != 0:
                    return False
            return True

    def test(self, x, y, x2, y2):
        if x == x2:
            return [4] if self.test_line(x, y, x2, y2, 0) else []
        elif y == y2:
            return [4] if self.test_line(x, y, x2, y2, 1) else []
        else:
            direction = int((x2 - x) > 0)
            ret = []
            margin = self.find_margin(x, y, direction)
            adjac = self.find_adj(margin[0], margin[1], direction)
            length = abs(margin[0] - adjac[0])
            if abs(x2 - x) < length and self.test_line(x, y, x2, y2, 0):
                ret.append(direction)
            else:
                direction = int((y2 - y) > 0) + 2
                margin = self.find_margin(x, y, direction)
                adjac = self.find_adj(margin[0], margin[1], direction)
                length = abs(margin[1] - adjac[1])
                if abs(y2 - y) < length and self.test_line(x, y, x2, y2, 1):
                    ret.append(direction)
            return ret

    def find_adj(self, x, y, direction):
        if direction == 0:
            for i in range(x-1, -1, -1):
                if self.table[i][y] != 0:
                    return i, y
            return -1, y
        elif direction == 1:
            for i in range(x+1, self.height):
                if self.table[i][y] != 0:
                    return i, y
            return self.height, y
        elif direction == 2:
            for j in range(y-1, -1, -1):
                if self.table[x][j] != 0:
                    return x, j
            return x, -1
        elif direction == 3:
            for j in range(y+1, self.width):
                if self.table[x][j] != 0:
                    return x, j
            return x, self.width
        return x, y

    def find_margin(self, x, y, direction):
        if direction == 0:
            for i in range(x, -1, -1):
                if i == 0 or self.table[i-1][y] == 0:
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
    
    def equal(self, coord1, coord2):    # test if two different cells are equal
        def cut(coord):
            coord = list(coord)
            if coord[0] < 0:
                coord[0] = 0
            if coord[0] > self.height - 1:
                coord[0] = self.height - 1
            if coord[1] < 0:
                coord[1] = 0
            if coord[1] > self.width - 1:
                coord[1] = self.width - 1
            return tuple(coord)
        coord1 = cut(coord1)
        coord2 = cut(coord2)
        return coord1 != coord2 and self.table[coord1[0]][coord1[1]] == self.table[coord2[0]][coord2[1]]
    
    def step(self, x, y, x2, y2, direction) -> bool:
        self.taken_step = True
        margin = self.find_margin(x, y, direction)
        if direction == 4:
            x_2, y_2 = x, y
        elif direction == 0:
            self.table[x2-x+margin[0]:x2+1, y] = self.table[margin[0]:x+1, y]
            self.table[max(margin[0], x2+1):x+1, y] = 0
            x_2, y_2 = x2, y
        elif direction == 1:
            self.table[x2:x2+margin[0]-x+1, y] = self.table[x:margin[0]+1, y]
            self.table[x:min(x2, margin[0]+1), y] = 0
            x_2, y_2 = x2, y
        elif direction == 2:
            self.table[x, y2-y+margin[1]:y2+1] = self.table[x, margin[1]:y+1]
            self.table[x, max(margin[1], y2+1):y+1] = 0
            x_2, y_2 = x, y2
        elif direction == 3:
            self.table[x, y2:y2+margin[1]-y+1] = self.table[x, y:margin[1]+1]
            self.table[x, y:min(y2, margin[1]+1)] = 0
            x_2, y_2 = x, y2
        left = self.find_adj(x_2, y_2, 2)   # find the leftmost non-blank cell after moving
        right = self.find_adj(x_2, y_2, 3)  # find the rightmost non-blank cell after moving
        up = self.find_adj(x_2, y_2, 0)     
        down = self.find_adj(x_2, y_2, 1)   
        choices = []    # record the multi-choice of the next step
        if self.equal(up, (x_2, y_2)) and direction in [2, 3, 4]:
            choices.append(up)
        if self.equal(down, (x_2, y_2)) and direction in [2, 3, 4]:
            choices.append(down)
        if self.equal(left, (x_2, y_2)) and direction in [0, 1, 4]:
            choices.append(left)
        if self.equal(right, (x_2, y_2)) and direction in [0, 1, 4]:
            choices.append(right)
        if len(choices) > 1:   # if there are multiple choices, return False
            return False
        # remove the matched two cells
        if direction == 4:
            self.table[x][y] = self.table[x2][y2] = 0
        elif direction in [0, 1]:
            self.table[x2][y2] = self.table[x2][y] = 0
        else:
            self.table[x2][y2] = self.table[x][y2] = 0
        return True

if __name__ == '__main__':
    table = NewTable(load_from_pic=True)
    table.show()
    print(table.actions)
'''↑:0 ↓:1 ←:2 →:3'''