# -*- coding: UTF-8 -*-
import re
import time
from datetime import datetime
from datetime import timedelta

from bs4 import BeautifulSoup

from biz.base_url_getter import BaseUrlGetter
from biz.verify.analyser import ManaulAnalyser, CodePlatformAnalyser
from request.request_helper import request
from util.constant import Constant
from util.selenium_util import get_selenium_driver, capture_verify_img


# 获取网页内容，如果需要验证码，就要解析
def get_url_content(url, img_id, code_input, sub_btn, account_name, verify_analyser_set):
    content = request.get(url).text
    # if "请输入验证码" not in content and "seccodeImage" not in content:
    if account_name in content:
        return content
    else:
        driver = get_selenium_driver()
        driver.get(url)
        # 如果是加密的页面，用浏览器打开就能正常解析，否则需要输入验证码
        if account_name in driver.page_source:
            return driver.page_source
        else:

            # 缓存title，用来验证是否页面跳转（验证码正确）
            temp_title = driver.title

            # 如果页面没有跳转，说明验证码有问题，需要重新输入
            analyser = None
            while driver.title == temp_title:

                if analyser is not None:
                    analyser.fail()

                # 首次或者分析器没机会了
                if not analyser:
                    analyser = verify_analyser_set.pop()

                print("使用%s校验，剩余%d次" % (analyser, analyser.retry_times))
                result = analyser.analyse(capture_verify_img(driver, img_id))
                if not result:
                    continue

                driver.find_element_by_id(code_input).send_keys(result)
                driver.find_element_by_id(sub_btn).click()
                time.sleep(5)  # 等待加载完成

            driver.implicitly_wait(10)
            return driver.page_source


# 从页面搜索列表中找出需要的公众号
def get_count_from_page(page_content, record):
    txt_box = BeautifulSoup(page_content, 'lxml').find_all("div", class_="txt-box")
    for box in txt_box:
        _a = box.find('a', uigs=re.compile('account_name_'))
        account = box.find('label', {'name': 'em_weixinhao'}).text

        # 如果有账号，就用这个判断，否则就用名字匹配，当然了，名字很不靠谱
        if ("account" in record and account == record['account']) or (
                        "account" not in record and _a.text == record['name']):
            return _a['href']
    return None


class AutoUrlGetter(BaseUrlGetter):
    """
    自动爬取公众号文章列表，不停的循环，每天爬一次
    1、搜狗搜索微信公众号名字
    2、找到对应的公众号链接
    3、进入链接，获取前十条数据
    """

    def action(self):
        print("开启自动爬取")
        base_url = "http://weixin.sogou.com/weixin?type=1&query=###&ie=utf8&_sug_=n&_sug_type_="
        while True:

            for record in self.biz_map_db.find_all():
                if 'last_update_time' in record and record['last_update_time'] > datetime.utcnow() - \
                        timedelta(hours=Constant.getConfig(Constant.SCRAWL_INTERVAL_HOUR)):
                    continue
                else:
                    # 来活了
                    print("开始爬取公众号", record['name'])
                    account_id = record['account'] if 'account' in record else record['name'];
                    page_content = get_url_content(
                        base_url.replace("###", account_id),
                        'seccodeImage', 'seccodeInput', 'submit', account_id,
                        [ManaulAnalyser(),
                         CodePlatformAnalyser(Constant.getConfig(Constant.VERIFY_CODE_MAP)['sougou'])])

                    artical_page_url = get_count_from_page(page_content, record)

                    if artical_page_url:
                        page_content = get_url_content(artical_page_url, 'verify_img', 'input', 'bt', account_id,
                                                       [ManaulAnalyser(), CodePlatformAnalyser(
                                                           Constant.getConfig(Constant.VERIFY_CODE_MAP)['penguin'])])
                        match_obj = re.findall(r'msgList =(.*?)\n', page_content)
                        if match_obj:
                            # 解析，然后修改爬取时间
                            self.dataAnalyse('str', match_obj[0], Constant.getConfig(Constant.WX_HIS_PAGE_PATH))
                            self.biz_map_db.db.update_one({'_id': record['_id']},
                                                          {'$set': {'last_update_time': datetime.utcnow()}})
                        else:
                            print('没找到文章数据')
                    else:
                        print("没有搜索到公众号")
                    time.sleep(60)
            time.sleep(60 * 10)
