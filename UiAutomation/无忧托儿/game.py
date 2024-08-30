import random
import numpy as np
from cv_digit import recognize_digit
import os

def set_seed(seed):
    random.seed(seed)

class Table:
    def __init__(self):
        self.width = 10
        self.height = 16
        # self.table = np.array([[random.randint(1, 9) for _ in range(self.width)] for _ in range(self.height)])
        for file in os.listdir('.'):
            if file.endswith('.jpg'):
                self.table = np.array(recognize_digit(file))
                break
        self.grade = 0
        self.operations = []

    def show(self, merge=None):
        str = ''
        for i, row in enumerate(self.table):
            for j, cell in enumerate(row):
                if cell == 0:
                    cell = ' '
                elif merge and merge[0] <= i <= merge[2] and merge[1] <= j <= merge[3]:
                    cell = '▢'
                str += f'{cell} '
            str += '\n'
        return str

    def merge(self, x_1, y_1, x_2, y_2, stop=False):
        x_min = min(x_1, x_2)
        x_max = max(x_1, x_2)
        y_min = min(y_1, y_2)
        y_max = max(y_1, y_2)
        sum = np.sum(self.table[x_min:x_max+1, y_min:y_max+1])
        if sum == 10:
            self.operations.append((x_min, y_min, x_max, y_max))
            self.grade += np.sum(self.table[x_min:x_max+1, y_min:y_max+1] > 0)
            if stop:
                print(f'current grade: {self.grade}, step: {(x_min, y_min, x_max, y_max)}')
                input(self.show([x_min, y_min, x_max, y_max]))
            self.table[x_min:x_max+1, y_min:y_max+1] = 0

def run(stop=False):
    table = Table()
    for _ in range(50000):
        x_1 = random.randint(0, 15)
        y_1 = random.randint(0, 9)
        x_2 = random.randint(0, 15)
        y_2 = random.randint(0, 9)
        table.merge(x_1, y_1, x_2, y_2, stop)
    return table

if __name__ == '__main__':
    max_grade = 0
    best_seed = 0
    for i in range(1):
        set_seed(i)
        grade = run().grade
        print(f'seed: {i}, grade: {grade}, max_grade: {max_grade}, best_seed: {best_seed}')
        if grade > max_grade:
            max_grade = grade
            best_seed = i

    set_seed(best_seed)
    table = run(stop=False)
    print(table.operations)