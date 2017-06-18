# -*- coding: UTF-8 -*-
from abc import ABCMeta
from abc import abstractmethod

from pymongo import MongoClient, errors

from util.constant import Constant


class BaseDb:
    __metaclass__ = ABCMeta

    def __init__(self, db, collection, timeout=300):

        try:
            self.client = MongoClient(port=int(Constant.getConfig("db_port")))[db]
            self.db = self.client[collection]
            self.timeout = timeout
        except errors.ConnectionFailure:
            print('数据库连接失败，程序退出')
            exit(-1)
            pass

    def __bool__(self):
        """"
            这个函数，我的理解是如果下面的表达式为真，则整个类为真
        """
        return True if self.db.find_one({'status': Constant.OUTSTANDING}) else False

    @abstractmethod
    def push(self, data):
        pass

    @abstractmethod
    def pop(self):
        pass

    def clear(self):
        self.db.drop()
