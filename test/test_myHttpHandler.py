# -*- coding: UTF-8 -*-
from unittest import TestCase

from myhttp import myserver
from myhttp.base_http_handler import BaseHttpHandler


class TestMyHttpHandler(TestCase):
    def test_do_POST(self):
        myserver.startHttp(8090, BaseHttpHandler)
