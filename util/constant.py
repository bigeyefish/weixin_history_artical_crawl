# -*- coding: UTF-8 -*-
import json
import os


class Constant:

    CONFIG = None

    # 配置文件路径
    CONFIG_FILE = os.path.dirname(os.path.abspath('__file__')) + '/resource/config.json'

    # http服务路径（类似servlet）
    WX_HIS_PAGE_PATH = 'wx_his_page_path'
    WX_HIS_JSON_PATH = 'wx_his_json_path'

    # 数据库配置
    DB_NAME = 'db_name'
    DB_ARTICALINFO_TABLE = 'db_articalinfo_table'
    DB_ARTICAL_TABLE = 'db_artical_table'
    DB_SOURCE_URL_TABLE = 'db_source_url_table'
    DB_BIZ_MAP_TABLE = 'db_biz_map_table'

    # 判断队列中记录是否爬取失败超时时间
    SCRAWL_TIMEOUT_SEC = 'scrawl_timeout_sec'

    # 爬取网页结果路径
    RESULT_PATH = "result_path"

    # 页面验证码存放路径
    VERIFY_CODE_PATH = "verify_code_path"

    # 线程从队列中获取爬取url间隔秒数
    THREAD_SLEEP_SEC = 'thread_sleep_sec'

    # 是否使用代理
    USE_PROXY = 'use_proxy'

    # url爬取状态，分别为：初始状态、正在下载、下载完成
    OUTSTANDING = 1
    PROCESSING = 2
    COMPLETE = 3
    FAILED = 4

    # 存储中间结果的目录
    TEMP_DIR = "temp_dir"

    # 超级鹰账户信息（打码平台）
    CHAOJIYING_ACCOUNT_INFO = "chaojiying_account_info"

    # 超级鹰验证码类型编码，本爬虫用到1、企鹅四位字母 2、搜狗6位数字+字母
    VERIFY_CODE_MAP = "verify_code_map"

    # 公众号两次爬取间隔（小时）
    SCRAWL_INTERVAL_HOUR = "scrawl_interval_hour"

    @classmethod
    def getConfig(cls, key):
        if not cls.CONFIG:
            cls.load()
        return cls.CONFIG[key]

    @classmethod
    def load(cls):
        print('加载配置文件')
        with open(cls.CONFIG_FILE) as json_file:
            cls.CONFIG = json.load(json_file)

