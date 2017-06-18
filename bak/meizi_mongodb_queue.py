from datetime import datetime, timedelta
from pymongo import MongoClient, errors


class MogoQueue:

    # 初始状态、正在下载、下载完成
    OUTSTANDING = 1
    PROCESSING = 2
    COMPLETE = 3

    def __init__(self, db, collection, timeout=300):
        self.client = MongoClient()[db]
        self.db = self.client[collection]
        self.timeout = timeout

    def __bool__(self):
        """"
            这个函数，我的理解是如果下面的表达式为真，则整个类为真
        """
        record = self.db.find_one({'status': {'$ne': self.COMPLETE}})
        return True if record else False

    def push(self, url, title):
        try:
            self.db.insert({'_id': url, 'status': self.OUTSTANDING, '主题': title})
            print(url, '插入队列成功')
        except errors.DuplicateKeyError as e:
            print(url, '已经存在于队列中了', e.details)
            pass

    def push_imgurl(self, title, url):
        try:
            self.db.insert({'_id': title, 'statue': self.OUTSTANDING, 'url': url})
            print('图片地址插入成功')
        except errors.DuplicateKeyError as e:
            print('地址已经存在了!', e.details)
            pass

    def pop(self):
        """
        这个函数会查询队列中所有状态为OUTSTANDING的值，更改状态，（query后面是查询)(update后面是更新),并返回_id（就是我们的URL)
        如果没有OUTSTANDING的值则调用repair()函数重置所有超时的状态为OUTSTANDING
        """
        record = self.db.find_one_and_update(
            filter={'status': self.OUTSTANDING},
            update={'$set': {'status': self.PROCESSING, 'timestamp': datetime.now()}}
        )

        if record:
            return record['_id']
        else:
            self.repair()
            raise KeyError

    def pop_title(self, url):
        record = self.db.find_one({'_id': url})
        return record['主题']

    def peek(self):
        record = self.db.find_one({'status': self.OUTSTANDING})
        if record:
            return record['_id']

    def complete(self, url):
        self.db.update({'_id': url}, {'$set': {'status': self.COMPLETE}})

    def repair(self):
        """
        这个函数是重置状态$lt是比较
        :return:
        """
        record = self.db.find_and_modify(
            query={'timestamp': {'$lt': datetime.now() - timedelta(seconds=self.timeout)}, 'status': self.PROCESSING},
            update={'$set': {'status': self.OUTSTANDING}}
        )

        if record:
            print('重置URL状态', record['_id'])

    def clear(self):
        self.db.drop()
