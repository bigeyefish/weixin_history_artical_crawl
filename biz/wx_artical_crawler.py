# -*- coding: UTF-8 -*-
import multiprocessing
import os
import re
import threading
import time

from bs4 import BeautifulSoup
from multiprocessing import Process
from datetime import datetime

from db.wx_mongodb_queue import WxMogoQueue
from request.request_helper import request
from util.constant import Constant
from util.str_util import mk_dir


def wx_artical_crawler(max_threads=1):
    crawl_queue = WxMogoQueue(Constant.getConfig(Constant.DB_NAME),
                              Constant.getConfig(Constant.DB_ARTICALINFO_TABLE),
                              Constant.getConfig(Constant.SCRAWL_TIMEOUT_SEC))
    artical = WxMogoQueue(Constant.getConfig(Constant.DB_NAME),
                          Constant.getConfig(Constant.DB_ARTICAL_TABLE),
                          Constant.getConfig(Constant.SCRAWL_TIMEOUT_SEC))

    def page_url_crawler():
        while True:
            try:
                record = crawl_queue.pop()
                artical_name = record['_id']
                print("开始爬取文章：%s" % artical_name)
            except KeyError:
                print('队列没有待爬去的数据了')
                break
            else:
                response = request.get(record['content_url'], 3)
                if not response:
                    print('[%s][%s]爬取失败，不再爬了' % (artical_name, record['content_url']))
                    crawl_queue.fail(artical_name)
                    continue
                soup = BeautifulSoup(response.text, 'lxml')
                date = soup.find(id='post-date')
                user = soup.find(id='post-user')

                try:

                    # 有的文章被和谐了
                    if not date or not user:
                        err_info = soup.find('p', class_="tips")
                        err_text = err_info and err_info.get_text() or record['content_url']
                        print("文章[%s]无效:%s" % (artical_name, err_text))
                    else:

                        # 公众号名字作为目录名
                        path = os.path.join(Constant.getConfig(Constant.RESULT_PATH), user.get_text().strip())
                        mk_dir(path)

                        # 文章中图片下载到本地
                        for _img in soup.find_all(attrs={"data-src": re.compile('mmbiz')}):
                            _img["src"] = saveImg(path, _img["data-src"])

                        # 文件名是日期开头加上文章名字
                        title = date.get_text() + ' ' + artical_name
                        save(soup.prettify(), path, title)

                        # 保存记录到文章表
                        artical.push({'biz_name': user.get_text(), 'title': title, 'date': date.get_text(),
                                      'author': record['author'], 'cover': record['cover'], 'digest': record['digest'],
                                      'timestamp': datetime.utcnow()})
                    crawl_queue.complete(artical_name)
                except IOError as e:
                    print("保存文件[%s]失敗:%s" % (artical_name, e))

            time.sleep(Constant.getConfig(Constant.THREAD_SLEEP_SEC))

    # 保存文件，文件名中有不合法的字符要去掉
    def save(req, path, title):
        print(u'开始保存:', title)
        title = re.sub(r'[\\/*?:|<>"]', '_', title)
        f = open(path + '/' + title + '.html', 'w', encoding='utf-8')
        f.write(req)
        f.close()

    # 保存文件中图片,文件名字为url中十六进制码
    # http://mmbiz.qpic.cn/mmbiz_png/ctwVEjeYQ28MO80FQ0lyibHqyYVXvPGicqDCngcmZicHVIdV4XPCc0VpJqarGxw8nB8C2GFmg41Unia7AiaZ52aiaFfA/0?wx_fmt=png
    def saveImg(path, img_url):
        match_obj = re.match(r'(.*)mmbiz(.*)/(.*?)/(.*)', img_url)
        if match_obj:

            img_type = match_obj.group(4).split('wx_fmt=')[1] if r'wx_fmt=' in match_obj.group(4) else 'jpg'
            name = match_obj.group(3) + '.' + img_type
            print(u'开始保存图片:', img_url)
            img = request.get(img_url, 3)
            f = open(path + '/' + name, 'ab')
            f.write(img.content)
            f.close()
            return name
        else:
            print(u'从图片url中获取十六进制码失败！')
            return None

    threads = []

    # 如果有线程在执行或者队列中还有待爬取得url，进程就继续干活
    # while threads or crawl_queue:
    while True:

        # is_alive是判断是否为空,不是空则在队列中删掉
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

        while len(threads) < max_threads and crawl_queue.peek():
            thread = threading.Thread(target=page_url_crawler())
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)

        time.sleep(Constant.getConfig(Constant.THREAD_SLEEP_SEC))


def process_crawler():
    """
    多进程启动程序
    :return:
    """
    process = []
    num_cpus = multiprocessing.cpu_count()
    print('将会启动进程数为:' + str(num_cpus))
    for i in range(num_cpus):
        p = Process(target=wx_artical_crawler())
        p.start()
        process.append(p)
    print('启动进程数：%d' % len(process))
    for p in process:
        # 等待进程队列里面的进程结束
        p.join()
