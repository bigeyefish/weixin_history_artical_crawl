# -*- coding: UTF-8 -*-
import re


class WxArtical:
    """微信文章json数据实体类"""

    def __init__(self, data):
        self.data = data

        # 用title当做mongodb的文档id
        data['_id'] = data['title']

        match_obj = re.match(r'(.*)_biz=(.*?)&amp;mid(.*?)', data['content_url']) if 'content_url' in data else None
        if match_obj:
            data['biz'] = match_obj.group(2)

        if not data['content_url'].startswith("http://mp.weixin.qq.com"):
            data['content_url'] = "http://mp.weixin.qq.com" + data['content_url']


