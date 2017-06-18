# -*- coding: UTF-8 -*-
import abc
from hashlib import md5

import requests

from util.constant import Constant


class Analyser:
    """验证码解析抽象类"""

    def __init__(self):
        # 默认校验失败尝试次数，负数一直校验（根本停不下来）
        self.retry_times = 3

    def __bool__(self):
        return self.retry_times != 0

    @abc.abstractmethod
    def analyse(self, img_path):
        return

    def fail(self):
        self.retry_times -= 1


class ManaulAnalyser(Analyser):
    """手动校验，后面集成到微信中去"""

    def __init__(self):
        self.retry_times = 0

    def analyse(self, img_path):
        return input("请输入验证码：(图片路径 %s)" % img_path)

    def __str__(self, *args, **kwargs):
        return "手动"


class CodePlatformAnalyser(Analyser):
    """打码平台校验，需要花money"""

    def __init__(self, codetype):
        super().__init__()
        account_info = Constant.getConfig(Constant.CHAOJIYING_ACCOUNT_INFO)
        self.username = account_info['username']
        self.password = md5(account_info['password'].encode('utf-8')).hexdigest()
        self.soft_id = account_info['soft_id']
        self.retry_times = account_info['retry_times']
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
            'codetype': codetype,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }
        self.codetype = codetype
        self.pic_id = ''

    def analyse(self, img_path):
        with open(img_path, 'rb') as fp:
            img_byte_data = fp.read()
        files = {'userfile': ('ccc.jpg', img_byte_data)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=self.base_params, files=files,
                          headers=self.headers)

        # {'str_debug': '', 'err_str': 'OK', 'pic_id': '48393453901', 'md5': '6de7695c7af94c9f53422ab191271ce9',
        # 'pic_str': 'zkbn', 'err_no': 0}
        result = r.json()
        self.pic_id = result['pic_id']
        if result['err_str'] == 'OK':
            return result['pic_str']
        else:
            print('打码失败：%s' % result['err_str'])
            return ''

    def __str__(self, *args, **kwargs):
        return "打码平台"

    def fail(self):
        super().fail()
        params = {'id': self.pic_id}
        params.update(self.base_params)
        try:
            r = requests.post('http://code.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        except Exception:
            pass
        print("打码错误，反馈平台。")


class OCRAnalyser(Analyser):
    """光学字符识别，能做出来就牛逼了"""

    def __init__(self):
        super().__init__()

    def analyse(self, img_path):
        super().analyse()

    def __str__(self, *args, **kwargs):
        return "OCR"

