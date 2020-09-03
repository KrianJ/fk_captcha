# -*- coding:utf-8 -*-
__Author__ = "KrianJ wj_19"
__Time__ = "2020/8/6 15:36"
__doc__ = """ 极验滑动验证码"""

# selenium组件
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
# 图像处理组件
from PIL import Image
from io import BytesIO
import time
from random import randint
# 自定义组件
from component.edge_detect import read_img, distance
from config import SLIDE_CONFIG, ACCOUNT, PASSWORD


class SlideCaptcha(object):
    def __init__(self, url, account, password):
        self.url = url
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)
        self.account = account
        self.password = password
        self.captcha_name = 'slide_captcha'

    def login(self):
        """登录"""
        self.browser.get(self.url)
        act_input = self.wait.until(EC.presence_of_element_located((By.XPATH, SLIDE_CONFIG['ACCOUNT_XPATH'])))
        pwd_input = self.wait.until(EC.presence_of_element_located((By.XPATH, SLIDE_CONFIG['PASSWORD_XPATH'])))
        # 由于是点击登录进行验证，相当于获取验证码button和登录button是一个button
        button = self.get_login_button()
        # 输入信息
        act_input.send_keys(self.account)
        pwd_input.send_keys(self.password)
        button.click()

        # 获取验证码图片
        self.get_captcha_image()
        # 根据距离移动滑块
        tracks = self._get_tracks()
        self._slide(tracks)

    def get_login_button(self):
        """获取验证码/登录按钮
        :return: button对象"""
        button = self.wait.until(EC.element_to_be_clickable((By.XPATH, SLIDE_CONFIG['SUBMIT_XPATH'])))
        return button

    def get_scrren_shot(self):
        """获取网页截图
        :return : 截图对象"""
        screen_shot = self.browser.get_screenshot_as_png()
        screen_shot = Image.open(BytesIO(screen_shot))
        return screen_shot

    def get_position(self):
        """获取验证码在截屏中的位置, 取对角线坐标(左上角(left,top)，右下角(right,bottom))
        :return: 位置信息 int(s)"""
        img = self.wait.until(EC.presence_of_element_located((By.XPATH, SLIDE_CONFIG['CAPTCHA_XPATH'])))
        time.sleep(1)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y']+size['height'], location['x'], location['x']+size['width']
        return top, bottom, left, right

    def get_captcha_image(self):
        """根据验证码位置获取截图中的验证码图片
        :return: image对象"""
        save_path = 'captcha/{0}/{1}.png'.format(self.captcha_name, self.captcha_name)
        # 截图获取带缺口图像
        top, bottom, left, right = self.get_position()
        print('验证码坐标位置(上,下,左,右): ', top, bottom, left, right)
        screenshot = self.get_scrren_shot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(save_path)
        # 获取完整图像
        return None

    def _get_slider(self):
        """获取滑块对象
        :return: 滑块对象"""
        slider = self.wait.until(EC.presence_of_element_located((By.XPATH, SLIDE_CONFIG['SLIDE_XPATH'])))
        return slider

    def _slide(self, tracks):
        """滑动滑块"""
        action = ActionChains(self.browser)
        slider = self._get_slider()
        action.click_and_hold(slider).perform()
        if type(tracks) == int:
            # 这是测试语句，一次移到指定位置
            action.move_by_offset(tracks, 0).perform()
        else:
            for track in tracks:
                action.move_by_offset(track, 0).perform()
                print('位移距离:', track, '当前x轴位置:', slider.location['x'])
                # 新建滑块防止累加唯一，否则每次位移量都是前几次的累加
                action = ActionChains(self.browser)
        action.release(on_element=None).perform()
    
    def _get_tracks(self):
        """获取滑块移动轨迹"""
        start_pos = 6
        img = read_img(self.captcha_name)
        end_pos = distance(img, filename=self.captcha_name)
        dis = end_pos-start_pos
        print('距离为', dis)
        # return dis

        tracks = []
        current = 0
        # 减速阈值,在滑到3/5处时减速
        mid = dis * 3 / 5
        # 计算间隔
        t = 0.5
        # 初速度
        v = 0
        while current < dis:
            if current < mid:
                # 加速度
                a = 10
            else:
                a = -10
            v0 = v
            v = v0 + a*t
            move = v0*t + 1/2 * a * t * t
            if (move + sum(tracks)) < dis:
                current += move
                tracks.append(round(move))
            else:
                current = dis
                tracks.append(dis - sum(tracks))
        print('轨迹为', tracks)
        return tracks


if __name__ == '__main__':
    s = SlideCaptcha(SLIDE_CONFIG['START_URL'], ACCOUNT, PASSWORD)
    s.login()







