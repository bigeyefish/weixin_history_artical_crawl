# -*- coding: UTF-8 -*-
from unittest import TestCase

from util.constant import Constant


class TestConstant(TestCase):
    def test_getConfig(self):
        print(Constant.getConfig('wx_his_page_path'))
