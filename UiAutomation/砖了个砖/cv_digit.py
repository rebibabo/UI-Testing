import os
import cv2
import numpy as np
from PIL import Image

def map(x, y):
    return int(y*112.8 + 92.5), int(x*113.7 + 581.2)

def find_matches(template_path, image_path):        # 模板匹配，返回匹配结果坐标
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where(res >= threshold)
    return zip(*loc[::-1])

def calculate(image1, image2):
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    max_vals = np.maximum(hist1, hist2)
    epsilon = 1e-10
    max_vals[max_vals == 0] = epsilon
    abs_diff = np.abs(hist1 - hist2)
    degree = np.sum(np.where(hist1 != hist2, 1 - abs_diff / max_vals, 1))
    degree = degree / len(hist1)
    return degree

def classify_hist_with_split(image1, image2, size=(256, 256)):
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data

def crop(ori_path, template_path, choice):      # 将图片裁剪到14*10的格子，并保存到template_path
    if choice == 0:     # 已知格子的范围
        image = Image.open(ori_path)
        pic_range = (36, 525, 1164, 2114)
        result = image.crop(pic_range)
        result.save(template_path)
    elif choice == 1:   # 通过opencv视觉自动确定格子的范围
        image = cv2.imread(ori_path)
        image = image[int(image.shape[0] * 0.18):int(image.shape[0] * 0.82), :] # 进行大致的裁剪
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转为灰度图
        edges = cv2.Canny(gray, 100, 200)   
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)   # 找出轮廓
        cv2.drawContours(image, contours, -1, (0, 255, 0), 2)   # 画出轮廓
        mask = np.zeros_like(gray)  # 创建掩码
        cv2.drawContours(mask, contours, -1, (255), -1) # 将轮廓填充到掩码中
        result = np.zeros_like(image)   # 创建结果图
        result[mask == 255] = image[mask == 255]    # 非掩码区域设置为黑色
        result = result[int(result.shape[0] * 0.026):int(result.shape[0] * 0.957), int(result.shape[1] * 0.03):int(result.shape[1] * 0.97)]
        cv2.imwrite(template_path, result)

def recognize_digit(ori_path):  # 识别图像
    print("recognizing picture...")
    img_path = 'image/image.jpg'
    crop(ori_path, img_path, 0)    # 裁剪图片
    image = Image.open(img_path)   # 打开裁剪的图片
    num_coord = [[0 for _ in range(10)] for _ in range(14)]
    max_index = len(os.listdir('image/')) - 1
    for i in range(1,  max_index):
        template_path = f'image/{i}.jpg'   # 打开模板图片，序号为i
        matches = find_matches(img_path, template_path) # 匹配模板，找到匹配结果坐标
        width, height = image.size
        cell_width = width / 10
        cell_height = height / 14
        for match in matches:   # 匹配节点的坐标转换为14*10的格子坐标
            x, y = match
            x = int(x / cell_width)
            y = int(y / cell_height)
            num_coord[y][x] = i
    empty_template = Image.open('image/0.jpg')   # 打开空白模板
    for i in range(14):
        for j in range(10):
            if num_coord[i][j] == 0:
                empty_block = image.crop((j*cell_width, i*cell_height, (j+1)*cell_width, (i+1)*cell_height))   # 裁剪出空白块
                similarity = calculate(np.array(empty_block), np.array(empty_template))   # 计算相似度
                if similarity < 0.3:
                    print(similarity)
                    print("new picture")    
                    x, y = map(i, j)    # 772 580
                    ori_img = Image.open(ori_path)
                    new_pic = ori_img.crop((x-45, y-45, x+45, y+45))   # 裁剪出新图片
                    new_pic.save(f'image/{max_index}.jpg')
                    num_coord[i][j] = max_index
    print("recognizing finished.")
    return num_coord

if __name__ == '__main__':
    num_coord = recognize_digit('screenshot.jpg')
    for each in num_coord:
        print(each)