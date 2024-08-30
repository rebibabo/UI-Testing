import cv2
import numpy as np
from PIL import Image

# pic_range = (47, 550, 1153, 2319)   
pic_range = (69, 585, 1129, 2279)  # 凑十消消消
# pic_range = (33, 452, 1043, 2059)

def find_matches(template_path, image_path):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    return zip(*loc[::-1])

def recognize_digit(ori_path):
    template_path = 'digits/template.jpg'
    image = Image.open(ori_path)
    image = image.crop(pic_range)
    image.save(template_path)
    num_coord = [[0 for _ in range(10)] for _ in range(16)]
    for i in range(1, 10):
        image_path = f'digits/{i}.jpg'
        matches = find_matches(template_path, image_path)
        width, height = image.size
        cell_width = width / 10
        cell_height = height / 16
        for match in matches:
            x, y = match
            x = int(x / cell_width)
            y = int(y / cell_height)
            num_coord[y][x] = i
    return num_coord

# print(recognize_digit('image.jpg'))