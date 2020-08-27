# -*- coding:utf-8 -*-
__Author__ = "KrianJ wj_19"
__Time__ = "2020/8/6 15:23"
__doc__ = """ 验证码配置信息"""

ACCOUNT = 'admin'
PASSWORD = 'admin'

# slide_captcha's config
SLIDE_CONFIG = {
    'START_URL': 'https://captcha1.scrape.center/',
    'ACCOUNT_XPATH': '//div[@class="el-form-item"][1]//input',                # input: 账户名
    'PASSWORD_XPATH': '//div[@class="el-form-item"][2]//input',               # input: 密码
    'SUBMIT_XPATH': '//div[3]/div/button',                                    # button: 登录/点击验证
    'CAPTCHA_XPATH': "//div[3]//canvas[2]",                                   # 验证码图片的xpath
    'SLIDE_XPATH': "//div[@class='geetest_panel_next']//div[@class='geetest_slider_button']"     # 滑块的xpath
}

# logoClick_captcha's config
LOGO_CLICK_CONFIG = {
    'START_URL': 'https://captcha2.scrape.center/',
    'ACCOUNT_XPATH': '//div[@class="el-form-item"][1]//input',                # input: 账户名
    'PASSWORD_XPATH': '//div[@class="el-form-item"][2]//input',               # input: 密码
    'SUBMIT_XPATH': '//div[3]/div/button',                                    # button: 登录/点击验证
    'CAPTCHA_XPATH': '//div[@class="geetest_window"]//img[@class="geetest_item_img"]',           # 验证码图片img标签
}

