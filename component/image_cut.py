# -*- coding:utf-8 -*-
__Author__ = "KrianJ wj_19"
__Time__ = "2020-09-03 16:28"
__doc__ = """ 图像分割：将logoClick验证码的参照图像分割"""

import cv2
import os
import numpy as np
from matplotlib import pyplot as plt


def get_logo(captcha_path: str):
    """获取验证码参考图标并通过二值化
    :param captcha_path: 下载的验证码图片路径
    :return type ndarray, 图标部分的图片矩阵"""
    threshold = 100
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
    """图像每列出现的黑色像素个数"""
    black_cnt = sum(logo_img == 0)

    """绘图"""
    # plt.hlines(4, 0, 120)
    plt.plot(black_cnt)
    plt.show()

    """分割logo_img"""
    local_min_index = []
    # 1. 先将明显划分的logo切割(即logo间有明显空隙)
    for i in range(len(black_cnt)-1):
        if black_cnt[i] and black_cnt[i+1] == 0:
            local_min_index.append(i+1)
        elif black_cnt[i-1] == 0 and black_cnt[i]:
            local_min_index.append(i)
    # print(local_min_index)

    # 2. 剔除空白区域
    intervals = []
    for j in range(len(local_min_index)-1):
        start = local_min_index[j]
        end = local_min_index[j+1]
        if max(black_cnt[start:end]):
            intervals.append([start, end])
    # print(intervals)

    # 3. 对有效区域进行阈值筛选，得到最终划分边界res
    res = []
    threshold = 2
    for interval in intervals:
        points = []
        temp = black_cnt[interval[0]: interval[1]]
        for j in range(len(temp)-1):
            if temp[j] < threshold and temp[j] < temp[j-1] and temp[j] < temp[j+1]:
                points.append(j)
        if points and points[0]:
            # 存在重叠部分
            points = [e+interval[0] for e in points]
            interval += points
        interval = sorted(interval)
        res += [[interval[i], interval[i+1]] for i in range(len(interval)-1)]
    print('logo的划分区间为：', res)

    # 4. 根据划分得到的区间分割logos
    logos = []
    for tmp in res:
        logo = logo_img[:, tmp[0]:tmp[1]+1]     # 这里+1，-1之类只是对分割的logo做适当调整
        logos.append(logo)
    return logos


def get_logos(captcha_path, save=False):
    logo_img = get_logo(captcha_path)
    logos = split_logo(logo_img)
    if save:
        save_logs(logos)
    return logos


def save_logs(logos: list):
    """
    将切割的图片保存
    :param logos:
    :return:
    """
    # 删除保存logo文件夹下所有之前的logo图片
    path = r'D:\Pyproject\fk_captcha\captcha\logoClick_captcha\logos'
    for file in os.listdir(path):
        file_path = path + '\\' + file
        os.remove(file_path)
    for i in range(len(logos)):
        filename = path + '\logo{0}.png'.format(str(i))
        cv2.imwrite(filename, logos[i])
    return None


if __name__ == '__main__':
    path = r'D:\Pyproject\fk_captcha\captcha\logoClick_captcha\logoClick_captcha_src.png'
    logo_img = get_logo(path)
    logos = split_logo(logo_img)
    save_logs(logos)

