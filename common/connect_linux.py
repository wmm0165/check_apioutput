# -*- coding: utf-8 -*-
# @Time : 2020/3/5 22:15
# @Author : wangmengmeng
import paramiko
from config.cfg import host, port, username, password

class ConLinux:

    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(host, port, username, password)

    def get_client(self):
        # ['root']['orders']['herb_medical_order']['herb_medical_order_info']['order_status']
        # stdout = self.client.exec_command('cat /tmp/hisresult/2020-03-05/H0003/receive_path/{}*.txt'.format(filename))[1]
        # content = stdout.read()
        # print(xmltodict.parse(content))
        return self.client




