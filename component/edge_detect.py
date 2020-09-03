# -*- coding:utf-8 -*-
__Author__ = "KrianJ wj_19"
__Time__ = "2020/8/6 18:16"
__doc__ = """ 图像边缘检测"""

import cv2
import pandas as pd
from PIL import Image
from matplotlib import pyplot as plt


def read_img(filename):
    # 转换成灰度图
    img = cv2.imread('captcha/{0}/{1}.png'.format(filename, filename), cv2.IMREAD_GRAYSCALE)

    # 写入灰度图和灰度矩阵，缺口处的灰度值相较其他较低
    cv2.imwrite('captcha/{0}/{1}_gray.png'.format(filename, filename), img)
    img = pd.DataFrame(img)
    img.to_csv('captcha/{0}/{1}.csv'.format(filename, filename))
    return img


# 二值化，阈值threshold, 顺便统计每一列的黑色像素个数
def distance(img, show=False, filename='captcha'):
    black_cnt = []
    threshold = 50
    for i in range(len(img.columns)):
        img.iloc[:, i][img.iloc[:, i] <= threshold] = 0
        img.iloc[:, i][img.iloc[:, i] > threshold] = 255
        black_cnt.append(list(img.iloc[:, i]).count(0))
    # 保存二值化图像
    # 显示二值化图像
    bin_img = img.values
    if show:
        cv2.imshow('new', bin_img)
        cv2.waitKey()
        cv2.destroyAllWindows()
    cv2.imwrite('captcha/{0}/{1}_bin.png'.format(filename, filename), bin_img)
    # 根据black_cnt生成增量数组
    inc_cnt = [black_cnt[i]-black_cnt[i-1] for i in range(1, len(black_cnt))]
    dis = inc_cnt.index(max(inc_cnt))
    return dis


if __name__ == '__main__':
    filename = 'captcha'
    img = read_img(filename=filename)
    dis = distance(img)
    print(dis)




