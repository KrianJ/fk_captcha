# -*- coding:utf-8 -*-
__Author__ = "KrianJ wj_19"
__Time__ = "2020-09-03 16:28"
__doc__ = """ 图像分割：将logoClick验证码的参照图像分割"""

import cv2
import os
import numpy as np


def get_logo(captcha_path: str):
    """获取验证码参考图标并通过二值化
    :param captcha_path: 下载的验证码图片路径
    :return type ndarray, 图标部分的图片矩阵"""
    threshold = 200
    img = cv2.imread(captcha_path, cv2.IMREAD_GRAYSCALE)
    logo_img = img[344:383, 0:116]    # [y0:y1, x0:x1]
    for i in range(logo_img.shape[0]):
        for j in range(logo_img.shape[1]):
            if logo_img[i, j] < threshold:
                logo_img[i, j] = 0
            else:
                logo_img[i, j] = 255
    # 保存处理后的图标
    cv2.imwrite(r'D:\Pyproject\fk_captcha\captcha\logoClick_captcha\logoClick__logo.png', logo_img)
    # 显示图标
    # cv2.imshow('image', logo_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return logo_img


def split_logo(logo_img: np.ndarray):
    """划分整个图标为单个图标
    :param logo_img: 二值化后的logo图片
    :return 分割后的单个图标列表"""
    # 每列出现的黑色像素个数
    black_cnt = sum(logo_img == 0)
    # 统计black_cnt中非零连续子数组的个数，根据其索引切割logos
    starts = []
    ends = []
    i = 1
    while i < len(black_cnt):
        if black_cnt[i-1] == 0 and black_cnt[i]:
            start = i
            i += 1
            starts.append(start)
            continue
        elif black_cnt[i] and black_cnt[i+1] == 0:
            end = i
            i += 1
            ends.append(end)
            continue
        i += 1
    # 切割logos
    logos = []
    for j in range(len(starts)):
        logo_j = logo_img[:, starts[j]-2:ends[j]+2]
        logos.append(logo_j)
    return logos


def get_logos(captcha_path):
    logo_img = get_logo(captcha_path)
    logos = split_logo(logo_img)
    return logos


if __name__ == '__main__':
    path = r'D:\Pyproject\fk_captcha\captcha\logoClick_captcha\logoClick_captcha_src.png'
    logo_img = get_logo(path)
    logos = split_logo(logo_img)
    print(logos[0].shape)
    for logo in logos:
        cv2.imshow('image', logo)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
