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
# 自定义组件
from slide_captcha import SlideCaptcha
from component.image_cut import get_logos
from config import LOGO_CLICK_CONFIG, ACCOUNT, PASSWORD


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
        logos = get_logos(save_path)
        return len(logos)


if __name__ == '__main__':
    a = LogoClickCaptcha(LOGO_CLICK_CONFIG['START_URL'], ACCOUNT, PASSWORD)
    a.login()

