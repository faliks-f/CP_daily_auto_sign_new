# -*- coding: utf-8 -*-
import random
import time

import cv2
import matplotlib.pyplot as plt
import numpy as np

i = 0


def get_timestamp_mil() -> int:
    now_time = time.time() * 1000 + random.randint(0, 999)
    return int(now_time)


def check_captcha(text):
    SIMPLE_CHAR_LIST = '134578ABCDEFHKNPQXYcfkxy'

    if len(text) != 4:
        return False

    for ch in text:
        if ch not in SIMPLE_CHAR_LIST:
            return False

    return True


def parse_img(inputs):
    """
    将输入转化为图片, 支持路径/numpy array/content(图片二进制).
    :param inputs: 任意输入
    :return: numpy array
    """
    if type(inputs) == str:
        return cv2.imread(inputs)
    elif type(inputs) == bytes:
        return cv2.imdecode(np.frombuffer(inputs, np.uint8), cv2.COLOR_RGBA2RGB)
    else:
        return inputs


def imshow(img):
    """
    转换奇怪的bgr和rgb
    :param img: numpy array
    """
    if len(img.shape) != 3:
        cv2.imwrite("./img.jpg", img)
        cv2.waitKey(1)
        plt.imshow(img)
        return

    cv2.imwrite("./img.jpg", img)
    cv2.waitKey(1)
    b, g, r = cv2.split(img)
    rgb = cv2.merge([r, g, b])
    plt.imshow(rgb)


def save(img):
    global i
    i += 1
    cv2.imwrite("data/" + str(i) + ".jpg", img)
    cv2.waitKey(1)
    print("save success number: " + str(i))
