#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import shutil
import urllib.parse
from http.server import BaseHTTPRequestHandler
from biz.base_url_getter import BaseUrlGetter

"""
httpserver,用于接收客服端传过来的数据
"""


class BaseHttpHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        mpath, margs = urllib.parse.splitquery(self.path)
        self.do_action(mpath, margs)

    def do_POST(self):
        mpath, margs = urllib.parse.splitquery(self.path)

        # 解析出请求数据
        enc = "UTF-8"
        datas = self.rfile.read(int(self.headers['content-length']))
        first_decode = urllib.parse.unquote(str(datas, enc), enc)
        param_arr = urllib.parse.parse_qsl(first_decode)

        # 调用业务逻辑
        self.responseData(self.do_action(mpath, param_arr))

    # 返回请求成功信息
    def do_action(self, path, param_arr):
        for key, value in param_arr:
            BaseUrlGetter().dataAnalyse(key, value, path)
        return "1"

    # 返回数据
    def responseData(self, data, enc='UTF-8'):

        content = data.encode(enc)
        f = io.BytesIO()
        f.write(content)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html;charset=%s" % enc)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)









