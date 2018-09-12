# -*- coding: utf-8 -*-
# 干掉知乎反爬流量验证码

import time
from TencentYoutuyun.youtu import YouTu
from zhihu import settings
from zhihu.tools import chromeDriver, OssUtils


def fuck_code():
    browser = chromeDriver.Chrome().get_driver()
    url = 'https://www.zhihu.com/account/unhuman?type=unhuman&message=%e7%b3%bb%e7%bb%9f%e6%a3%80%e6%b5%8b%e5%88%b0%e6%82%a8%e7%9a%84%e5%b8%90%e5%8f%b7%e6%88%96IP%e5%ad%98%e5%9c%a8%e5%bc%82%e5%b8%b8%e6%b5%81%e9%87%8f%ef%bc%8c%e8%af%b7%e8%bf%9b%e8%a1%8c%e9%aa%8c%e8%af%81%e7%94%a8%e4%ba%8e%e7%a1%ae%e8%ae%a4%e8%bf%99%e4%ba%9b%e8%af%b7%e6%b1%82%e4%b8%8d%e6%98%af%e8%87%aa%e5%8a%a8%e7%a8%8b%e5%ba%8f%e5%8f%91%e5%87%ba%e7%9a%84&need_login=true'
    try:
        browser.get(url)
        time.sleep(3)
        if browser.current_url != url:
            return
        # 获取验证码图片
        img = browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/section/div/img')
        img_base_64 = img.get_attribute('src').replace('data:image/png;base64,', '').replace('%0A', '')
        # 识别验证码获得结果
        code = solve_code(img_base_64)
        # 填入验证码
        input = browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/section/div/div/input')
        input.send_keys(code)
        # 点击验证按钮
        button = browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/section/button')
        button.click()
    finally:
        browser.close()


def solve_code(img_base_64):
    img_name = OssUtils.upload_img(img_base_64)
    client = YouTu(settings.APP_ID, settings.API_KEY, settings.API_SECRET)
    res = client.generalocr(settings.OSS_URL.format(img_name), data_type=1)
    try:
        return res['items'][0]['itemstring']
    except Exception:
        return "error"