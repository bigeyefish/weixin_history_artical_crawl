# -*- coding: UTF-8 -*-

import json
from json import JSONDecodeError
import os


# 去掉字符串中换行符
def escapeStr(data):
    return str(data).replace('''\r''', '').replace('''\n''', '').replace(r'&amp;', '&').replace(r'amp;', '').replace(r'&nbsp;', ' ')


# 如果字符串中含有引号，则替换掉,否则转换会报错
def decode2Json(data):
    try:
        return json.loads(data)
    except JSONDecodeError as e:
        print("转json出错,再试一下：[%s][%s]" % (data, e))
        # list:[]数据中包含的引号要去掉
        data = data[:data.index('[')] + data[data.index('['): data.rindex(']')].replace(r'\"', '#*#*#').replace(r'"',"_").replace('#*#*#', r'\"') + data[data.rindex(']'):]
        return json.loads(data.replace("&quot;", "\""))


def mk_dir(path):
    if not os.path.exists(path):
        print(u'建了一个名字叫做', path, u'的文件夹!')
        os.makedirs(path)