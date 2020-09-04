# -*- coding:utf-8 -*-
__Author__ = "KrianJ wj_19"
__Time__ = "2020/8/27 15:38"
__doc__ = """ 图标点选验证码"""

# selenium组件
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
# 通用组件
import time
import requests
import json
# 自定义组件
from slide_captcha import SlideCaptcha
from component.image_cut import get_logos
from component.chaojiying import Chaojiying_Client
from config import *


class LogoClickCaptcha(SlideCaptcha):
    def __init__(self, url, account, password):
        super(LogoClickCaptcha, self).__init__(url=url, account=account, password=password)
        self.captcha_name = 'logoClick_captcha'

    def login(self):
        self.browser.get(self.url)
        act_input = self.wait.until(EC.presence_of_element_located((By.XPATH, LOGO_CLICK_CONFIG['ACCOUNT_XPATH'])))
        pwd_input = self.wait.until(EC.presence_of_element_located((By.XPATH, LOGO_CLICK_CONFIG['PASSWORD_XPATH'])))
        # 由于是点击登录进行验证，相当于获取验证码button和登录button是一个button
        button = self.get_login_button()
        # 输入信息并登录
        act_input.send_keys(self.account)
        pwd_input.send_keys(self.password)
        button.click()

        # 获取验证码
        self.get_captcha_image()
        logos = self.get_captcha_logos()

        # 识别logos在浏览器显示的位置
        logo_positions, offsets = self.get_logo_position(cjy=True)
        # 模拟点击
        for pos in offsets:
            self.click_position(pos)
            time.sleep(1)
        # 点击确认完成验证
        submit_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, LOGO_CLICK_CONFIG['SUBMIT_CAPTCHA'])))
        submit_btn.click()

    def get_login_button(self):
        """获取验证码/登录按钮
        overwrite: 修改xpath"""
        button = self.wait.until(EC.element_to_be_clickable((By.XPATH, LOGO_CLICK_CONFIG['SUBMIT_XPATH'])))
        return button

    def get_position(self):
        """获取验证码在截屏中的位置, 取对角线坐标(左上角(left,top)，右下角(right,bottom))
        overwrite: 修改xpath"""
        img = self.wait.until(EC.presence_of_element_located((By.XPATH, LOGO_CLICK_CONFIG['CAPTCHA_XPATH'])))
        location = img.location
        size = img.size
        # (x,y)图片左上角坐标，通过x，y轴上的四条直线确定一个矩形
        top, bottom, left, right = location['y'], location['y']+size['height'], location['x'], location['x']+size['width']
        return top, bottom, left, right

    def get_captcha_logos(self):
        """通过图片链接下载验证码图片"""
        captcha = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, LOGO_CLICK_CONFIG['CAPTCHA_XPATH'])))
        url = captcha.get_attribute('src')
        img = requests.get(url).content
        save_path = 'captcha/{0}/{1}_src.png'.format(self.captcha_name, self.captcha_name)
        with open(save_path, 'wb') as f:
            f.write(img)
        logos = get_logos(save_path, save=True)
        return logos

    def get_logo_position(self, cjy=False):
        """获取logo在验证码中的位置
        :param cjy 是否使用超级鹰平台
        :returns logos_pos: logo的坐标, offsets: logo之间的偏移量"""
        if cjy:
            logos_pos = []

            # 通过cjy获取logo在验证码上的坐标
            client = Chaojiying_Client(CJY_ACC, CJY_PWD, CJY_ID)
            img = open(r'D:\Pyproject\fk_captcha\captcha\logoClick_captcha\logoClick_captcha_src.png', 'rb').read()
            positions = client.PostPic(img, CJY_CAPTCHA_TYPE)['pic_str']
            print("超级鹰返回结果：", positions)

            # 对坐标格式化，获取logo在网页的点击坐标
            positions = positions.split('|')
            positions = [ele.split(',') for ele in positions]
            top, _, left, _ = self.get_position()           # 验证码图片在网页的坐标
            for pos in positions:
                # logo在网页的坐标
                logo_pos = [left+int(pos[0]), top+int(pos[1])]
                logos_pos.append(logo_pos)

            # 计算偏移量
            offsets = [logos_pos[0]]
            for i in range(1, len(logos_pos)):
                x_offset = logos_pos[i][0] - logos_pos[i-1][0]
                y_offset = logos_pos[i][1] - logos_pos[i-1][1]
                offsets.append([x_offset, y_offset])

            print("图标的点击坐标分别是：", logos_pos)
            print("坐标点击的偏移量为：", offsets)
            return logos_pos, offsets
        else:
            pass

    def click_position(self, position, left_click=True):
        """模拟点击指定坐标"""
        action = ActionChains(self.browser)
        # 鼠标点击坐标是累加的，每点击一次都要重新建立action
        if left_click:
            action.move_by_offset(position[0], position[1]).click().perform()
        else:
            action.move_by_offset(position[0], position[1]).context_click().perform()
        print('完成一次点击')
        return None


if __name__ == '__main__':
    a = LogoClickCaptcha(LOGO_CLICK_CONFIG['START_URL'], ACCOUNT, PASSWORD)
    a.login()

