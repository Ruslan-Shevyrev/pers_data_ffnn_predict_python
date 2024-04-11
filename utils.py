import numpy as np
import config.config as config


def str_to_arr(list_str):
    list_num = np.zeros(config.INPUT_SIZE, np.float32)

    for i, list_char in enumerate(list_str, start=0):
        list_num[i] = ord(list_char)

    return list_num
