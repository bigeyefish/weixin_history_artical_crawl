#!/usr/bin/python
# -*- coding: UTF-8 -*-
from unittest import TestCase
from request.proxyip_util import proxyIpUtil


class TestProxyIpUtil(TestCase):
    def test_get_ips(self):
        print(''.join(proxyIpUtil.get_random_ip()))
