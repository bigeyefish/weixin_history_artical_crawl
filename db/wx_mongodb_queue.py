#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from pymongo import errors

from db.base_db import BaseDb
from util.constant import Constant


class WxMogoQueue(BaseDb):
    # 如果不存在直接插入，如果存在并且没有爬取完成并且url不同，则更新url
    def push(self, data):
        try:
            # 文章信息
            if 'content_url' in data:
                record = self.db.find_one({"_id": data["_id"]})
                if not record:
                    self.db.insert(dict(data, **{'status': Constant.OUTSTANDING}))
                    print(data['_id'], '插入队列成功')
                elif record['content_url'] != data['content_url'] and record['status'] != Constant.COMPLETE:
                    self.db.update_one({"_id": data["_id"]},
                                       {"$set": {"content_url": data['content_url'], "status": Constant.OUTSTANDING}})
                    print(data['_id'], '更新url地址')
            else:
                self.db.insert(data)
        except errors.DuplicateKeyError as e:
            print(data['title'], '已经存在于队列中了', e.details)
            pass

    def pop(self):
        """
        这个函数会查询队列中所有状态为OUTSTANDING的值，更改状态，（query后面是查询)(update后面是更新),并返回_id
        如果没有OUTSTANDING的值则调用repair()函数重置所有超时的状态为OUTSTANDING
        """
        record = self.db.find_one_and_update(
            filter={'status': Constant.OUTSTANDING},
            update={'$set': {'status': Constant.PROCESSING, 'timestamp': datetime.utcnow()}}
        )

        if record:
            return record
        else:
            self.repair()
            raise KeyError

    def peek(self):
        record = self.db.find_one({'status': Constant.OUTSTANDING})
        return record['_id'] if record else None

    def complete(self, _id):
        self.db.update({'_id': _id}, {'$set': {'status': Constant.COMPLETE}})

    def fail(self, _id):
        self.db.update({'_id': _id}, {'$set': {'status': Constant.FAILED}})

    def repair(self):
        """
        这个函数是重置状态$lt是比较
        :return:
        """
        record = self.db.find_and_modify(
            query={'timestamp': {'$lt': datetime.utcnow() - timedelta(seconds=self.timeout)},
                   'status': Constant.PROCESSING},
            update={'$set': {'status': Constant.OUTSTANDING}}
        )

        if record:
            print('重置URL状态', record['_id'])

    def find_all(self):
        return self.db.find({})
