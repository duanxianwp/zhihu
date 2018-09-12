''' test Selenium + Chrome'''
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Chrome:
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    USER_AGENTS = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
    ]
    driver = None

    def __init__(self):
        # 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
        self.dcap["chrome.page.settings.userAgent"] = (random.choice(self.USER_AGENTS))
        # 不载入图片，爬页面速度会快很多
        self.dcap["chrome.page.settings.loadImages"] = False
        # 设置代理
        # self.service_args = ['--proxy=127.0.0.1:8888', '--proxy-type=http']

    def get_driver(self):
        if self.driver is None:
            chrome_options = Options()
           # chrome_options.add_argument('--headless')
           # chrome_options.add_argument('--disable-gpu')
            self.driver = webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=self.dcap)
        return self.driver
