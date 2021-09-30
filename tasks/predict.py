# -*- coding: utf-8 -*-
import os

import cv2
import numpy as np
import paddle.inference as pi

# from predict.utils import parse_img
from predict.utils import parse_img

CHANNEL, HEIGHT, WIDTH = (3, 34, 92)
CHAR_LIST = '12345678ABCDEFHKNPQXYZabcdefhknpxyz'

_now_path = os.path.dirname(__file__)
MODEL_PATH = os.path.join(_now_path, 'models', 'inference.pdmodel')
PARAMS_PATH = os.path.join(_now_path, 'models', 'inference.pdiparams')

print(MODEL_PATH)

_config = pi.Config(MODEL_PATH, PARAMS_PATH)
_predictor = pi.create_predictor(_config)

if CHANNEL == 1:
    def pre_process(img):
        _, binary = cv2.threshold(img, 0x70, 1, cv2.THRESH_BINARY)
        binary = binary[:, :, 0]
        return np.array(binary, dtype='float32').reshape((1, HEIGHT, WIDTH))
elif CHANNEL == 3:
    def pre_process(img):
        return np.array(img, dtype='float32').reshape([CHANNEL, HEIGHT, WIDTH]) / 255
else:
    print('error, cannot pre_process img like this.')


def ctc_decode(text, blank=len(CHAR_LIST)):
    result = []
    cache_idx = -1
    for char in text:
        if char != blank and char != cache_idx:
            result.append(char)
        cache_idx = char
    return result


def label_arr2text(arr):
    return ''.join([CHAR_LIST[ch] for ch in arr])


def predict_captcha(img):
    img = parse_img(img)
    img = pre_process(img)
    img = np.expand_dims(img, axis=0)

    input_names = _predictor.get_input_names()
    input_handle = _predictor.get_input_handle(input_names[0])
    input_handle.reshape([1, 1, HEIGHT, WIDTH])
    input_handle.copy_from_cpu(img)
    _predictor.run()

    output_names = _predictor.get_output_names()
    output_handle = _predictor.get_output_handle(output_names[0])
    output_data = output_handle.copy_to_cpu()
    return label_arr2text(ctc_decode(output_data[0]))
