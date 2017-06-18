# -*- coding: UTF-8 -*-
import threading
from biz.auto_url_getter import AutoUrlGetter
from biz.wx_artical_crawler import process_crawler
from myhttp import myserver
from myhttp.base_http_handler import BaseHttpHandler
from util.constant import Constant
from util.str_util import mk_dir


def init():
    """初始化环境"""

    mk_dir(Constant.getConfig(Constant.TEMP_DIR))  # 创建临时目录文件夹

if __name__ == "__main__":
    init()
    threading.Thread(target=AutoUrlGetter().action, daemon=True).start()
    threading.Thread(target=lambda: myserver.startHttp(8090, BaseHttpHandler), daemon=True).start()
    process_crawler()

    # myserver.startHttp(8090, WxHttpHandler)
