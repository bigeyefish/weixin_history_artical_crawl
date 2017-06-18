# -*- coding: UTF-8 -*-
import random

from PIL import Image
from selenium import webdriver
import os

from selenium.common.exceptions import NoSuchElementException

from util.constant import Constant

driver = None


def get_selenium_driver():
    global driver
    if not driver:
        print("需要输入验证码才行，用selenium加载PhantomJS引擎渲染页面")
        # chromedriver = r'D:\tools\chromedriver.exe'
        # os.environ["webdriver.chrome.driver"] = chromedriver
        driver = webdriver.PhantomJS()
    return driver


def close_driver():
    driver.close()
    driver.quit()


def capture_verify_img(driver, img_id):
    """页面验证码截图"""

    try:
        img_ele = driver.find_element_by_id(img_id)
    except NoSuchElementException:
        print(driver.page_source)
        pass

    if img_ele:

        # 由于验证码src是一个动态的，每次访问都不同，所以利用selenium截图出来，然后再处理
        driver.get_screenshot_as_file(os.path.join(Constant.getConfig(Constant.TEMP_DIR), "screenshot.jpg"))
        x, y = img_ele.location['x'], img_ele.location['y']
        width, height = img_ele.size['width'], img_ele.size['height']
        region = Image.open(os.path.join(Constant.getConfig(Constant.TEMP_DIR), "screenshot.jpg")) \
            .crop((x, y, x + width, y + height))

        img_path = os.path.join(Constant.getConfig(Constant.VERIFY_CODE_PATH), str(random.randint(10000, 99999)) + '.jpg')
        region.save(img_path)
        region.close()

        return img_path
    else:
        raise BaseException("页面不存在验证码ID的Element，这是毛线页面")



