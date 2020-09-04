# Crack Log
## 2020.08.27
### 完成滑动验证码破解
* 1.slide_captcha.py:
    ** Define class named SlideCaptcha.
    ** Before using, update the SLIDE_CONFIG in config.py, which includes necessary xpath paths.
    ** After that, create the instance, call login() function.
* 2.Intermediate file:
    Sub diretory -- "slide_captcha" of captcha directory.
        .csv: captcha image's gray level matrix
        .png: captcha image
        xx_bin.png: binary version.
        xx_gray.png: gray version.

## 2020.09.04
### 完成图标点击验证码破解(超级鹰版本)
* 1.logoClick_captcha.py:
    ** Define class named LogoClickCaptcha.
    ** Before using, update the SLIDE_CONFIG in config.py, which includes necessary xpath paths.
    ** After that, create the instance, call login() function.
* 2.Intermediate file:
    All files start with "slide_captcha" in directory captcha.
        logos(dir): logos cut from 'logoClick_logo.png'
        logoClick_logo.png: cut from 'logoClick_captcha_src.png'
        logoClick_captcha.png: cropped from screenshot
        logoClick_captcha_src.png: downloaded from src in tag's src attribute of the captcha.
### Unfinished: 完成图标点击验证码破解(自己的版本)
* Stuck Point: 对提取处来的logo进行定位(Get the location of the icons, in logos folder, on the logoClick_captcha_src.png)
* Other Tips: Once Solved, the param cjy will no longer to be True.
