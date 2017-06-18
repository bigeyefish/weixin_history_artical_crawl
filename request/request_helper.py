# -*- coding: UTF-8 -*-
import time

import requests

from request.agent_util import agentUtil
from request.proxyip_util import proxyIpUtil
from util.constant import Constant


# util class used to net work data request
class MyRequest:
    def get(self, url, timeout=6, proxy=False, num_retries=6):  # 给函数一个默认参数proxy为空

        headers = {
            'User-Agent': agentUtil.get_random_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }

        # 默认不使用代理
        if not proxy:
            try:
                return requests.get(url, headers=headers, timeout=timeout)
            except:

                # num_retries是我们限定的重试次数
                if num_retries > 0:
                    time.sleep(10)
                    print(u'获取网页出错，10S后将获取倒数第：', num_retries, u'次')
                    return self.get(url, timeout, num_retries=num_retries - 1)  # 调用自身 并将次数减1
                elif Constant.USE_PROXY:
                    print(u'开始使用代理')
                    time.sleep(10)

                    return self.get(url, timeout, True, )
                else:
                    print(u'爬取失败了[%s]' % url)
                    return None

        else:  # 当代理不为空
            try:
                proxy = {'http': 'http://'.join(proxyIpUtil.get_random_ip())}
                print(u'当前代理是：', proxy['http'])
                return requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
            except:

                if num_retries > 0:
                    time.sleep(10)
                    print(u'正在更换代理，10S后将重新获取倒数第', num_retries, u'次')
                    return self.get(url, timeout, True, num_retries - 1)
                else:
                    print(u'代理也不好使了！放弃了！[', url, ']')
                    # return self.get(url, 3)


request = MyRequest()
