# -*- coding: UTF-8 -*-
from http.server import HTTPServer


# 启动http服务
def startHttp(port, clazz):

    httpd = HTTPServer(('localhost', port), clazz)
    print(u"http服务启动成功，端口号：", port)
    httpd.serve_forever()

