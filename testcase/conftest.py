# -*- coding: utf-8 -*-
# @Time : 2020/3/6 0:44
# @Author : wangmengmeng
import pytest
from common.connect_linux import ConLinux
from common.send_data import SendData
@pytest.fixture(scope='module')
def get_conn():
    cl = ConLinux()
    yield cl.get_client()

@pytest.fixture(scope='function')
def send():
    sd = SendData()
    yield sd