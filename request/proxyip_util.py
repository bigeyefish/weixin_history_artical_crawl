# -*- coding: UTF-8 -*-
import requests
import re
import datetime
import os
import random


class ProxyIpUtil:
    def __init__(self):
        self.proxyIpUrl = "myhttp://haoip.cc/tiqu.htm"
        self.proxy_static_file = os.path.dirname(os.path.abspath('__file__')) + '\\resource\\temp_proxy_ip.txt'
        self.proxy_ip_list = []

    def get_random_ip(self):

        if len(self.proxy_ip_list) == 0:

            print(datetime.datetime.now(), u"开始获取代理IP列表")

            try:
                html = requests.get(self.proxyIpUrl)
            except IOError as e:
                print(datetime.datetime.now(), u"获取代理IP列表失败，从缓冲文件中获取", e)

                try:
                    for line in open(os.path.abspath(self.proxy_static_file)):
                        self.proxy_ip_list.append(line.replace('\n', ''))
                except IOError as e1:
                    print(datetime.datetime.now(), u"悲催，读取文件也失败了，这里不适合你，放弃吧！！", e1)
                else:
                    print(datetime.datetime.now(), u"从文件中获取代理IP列表成功,", len(self.proxy_ip_list), u"个")
            else:
                # 正则表示从html.text中获取所有r/><b中的内容，re.S的意思是包括匹配包括换行符，findall返回的是个list哦！
                for ip in re.findall(r'r/>(.*?)<b', html.text, re.S):
                    # re.sub 是re模块替换的方法，这儿表示将\n替换为空
                    i = re.sub('\n', '', ip)
                    self.proxy_ip_list.append(i.strip())
                print(datetime.datetime.now(), u"获取代理IP列表成功，", len(self.proxy_ip_list))

        return random.choice(self.proxy_ip_list)


proxyIpUtil = ProxyIpUtil()
