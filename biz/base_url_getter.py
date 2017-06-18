# -*- coding: UTF-8 -*-
"""
获取数据，解析url并入库抽象类
"""
import json

from db.wx_mongodb_queue import WxMogoQueue
from util.constant import Constant
from util.str_util import decode2Json
from model.wx_artical import WxArtical
from util.str_util import escapeStr


class BaseUrlGetter:
    def __init__(self):
        self.artical_db = WxMogoQueue(Constant.getConfig(Constant.DB_NAME),
                                      Constant.getConfig(Constant.DB_ARTICALINFO_TABLE),
                                      Constant.getConfig(Constant.SCRAWL_TIMEOUT_SEC))
        self.source_url_db = WxMogoQueue(Constant.getConfig(Constant.DB_NAME),
                                         Constant.getConfig(Constant.DB_SOURCE_URL_TABLE),
                                         Constant.getConfig(Constant.SCRAWL_TIMEOUT_SEC))
        self.biz_map_db = WxMogoQueue(Constant.getConfig(Constant.DB_NAME),
                                      Constant.getConfig(Constant.DB_BIZ_MAP_TABLE),
                                      Constant.getConfig(Constant.SCRAWL_TIMEOUT_SEC))

    # 解析获取的数据
    @staticmethod
    def analysePageData(data, path):
        json_data = []
        if path == Constant.getConfig(Constant.WX_HIS_PAGE_PATH):
            data_obj = decode2Json(data[1:-1].replace(r'\\', ''))
            json_data = [entity['app_msg_ext_info'] for entity in data_obj['list'] if 'app_msg_ext_info' in entity]

        elif path == Constant.getConfig(Constant.WX_HIS_JSON_PATH):
            data_obj = decode2Json(data)
            if data_obj['errmsg'] != 'ok':
                print(u'获取数据错误：', data_obj['errmsg'])
            json_data = [entity['app_msg_ext_info'] for entity in json.loads(data_obj['general_msg_list'])['list'] if
                         'app_msg_ext_info' in entity]

        # 一起的文章拆分开
        result = []
        for element in json_data:
            if element['title']:
                result.append(element)
            if element['is_multi'] == 1:
                result += [x for x in element['multi_app_msg_item_list'] if x['title']]
        print(u"获取", len(result), u"条待爬数据")
        return result

    # 对获取的带url的数据进行解析处理并入库
    def dataAnalyse(self, key, value, path):
        if key == 'str':
            for data in self.analysePageData(escapeStr(value), path):
                self.artical_db.push(WxArtical(data).data)
        elif key == 'url':
            # 直接入库
            self.source_url_db.push({"url": value, "title": value})
