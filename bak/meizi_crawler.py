import multiprocessing
import os
import threading
import time

from bs4 import BeautifulSoup

from bak.meizi_mongodb_queue import MogoQueue
from request.request_helper import request

SLEEP_TIME = 1


def mzitu_crawler(max_threads=10):
    crawl_queue = MogoQueue('meinvxiezhenji', 'crawl_queue')

    def page_url_crawler():
        while True:
            try:
                url = crawl_queue.pop()
                print(url)
            except KeyError:
                print('队列没有数据')
                break
            else:
                img_urls = []
                req = request.get(url, 3).text
                title = crawl_queue.pop_title(url)
                mkdir(title)
                os.chdir('d:\mzitu\\' + title)
                max_span = BeautifulSoup(req, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
                for page in range(1, int(max_span) + 1):
                    page_url = url + '/' + str(page)
                    img_url = \
                    BeautifulSoup(request.get(page_url, 3).text, 'lxml').find('div', class_='main-image').find('img')[
                        'src']
                    img_urls.append(img_url)
                    save(img_url)

                crawl_queue.complete(url)

    def save(img_url):
        name = img_url[-9:-4]
        print(u'开始保存:', img_url)
        img = request.get(img_url, 3)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def mkdir(path):
        path = path.strip()
        isExists = os.path.exists(os.path.join("d:\mzitu", path))
        if not isExists:
            print(u'建了一个名字叫做', path, u'的文件夹!')
            os.makedirs(os.path.join("d:\mzitu", path))
            return True
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了!')
            return False

    threads = []

    # 如果有线程在执行或者队列中还有待爬取得url，进程就继续干活
    while threads or crawl_queue:

        # is_alive是判断是否为空,不是空则在队列中删掉
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

        while len(threads) < max_threads and crawl_queue.peek():
            thread = threading.Thread(target=page_url_crawler())
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)

        time.sleep(SLEEP_TIME)
    print(u'进程[', os.getpid(), u']干完活了！')


def process_crawler():
    """
    多进程启动程序
    :return:
    """
    process = []
    num_cpus = multiprocessing.cpu_count()
    print('将会启动进程数为:' + str(num_cpus))
    for i in range(num_cpus):
        p = multiprocessing.Process(target=mzitu_crawler())
        p.start()
        process.append(p)
    for p in process:
        # 等待进程队列里面的进程结束
        p.join()


if __name__ == "__main__":
    process_crawler()
