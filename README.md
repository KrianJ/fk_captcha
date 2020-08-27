# Crack Log
## 2020.8.27
### 完成滑动验证码破解
* 1.slide_captcha.py:
    Define class named SlideCaptcha, Before using, update the SLIDE_CONFIG in config.py
which includes necessary xpath paths. After that, create the instance, call login() function.
* 2.Middle file:
    All files start with "slide_captcha" in directory captcha.
    .csv: captcha image's gray level matrix
    .png: captcha image
    xx_bin.png: binary version.
    xx_gray.png: gray version.