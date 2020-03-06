# -*- coding: utf-8 -*-
# @Time : 2020/3/5 23:11
# @Author : wangmengmeng
from config.cfg import url_normal
import requests
import os
import time, random
from datetime import datetime

class SendData:
    def __init__(self):
        ts = int(time.mktime(time.strptime(datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")))
        change_after = ts + random.randint(1, 10000000)
        self.change_data = {"{{ts}}": str(change_after),
                       "{{gp}}": str(change_after),
                       "{{zyhzh}}": str(change_after),
                       "{{mzhzh}}": str(change_after),
                       "{{dt}}": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                       "{{d2}}": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                       }
    def post_xml(self,url,xmlname):
        xml_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', xmlname)
        headers = {"Content-Type": "text/plain"}

        with open(xml_path, encoding="utf-8") as fp:
            body = fp.read()
        ss = body
        for k in self.change_data:
            ss = ss.replace(k, self.change_data[k])
        print(ss)
        res = requests.post(url, data=ss.encode("utf-8"), headers=headers)
        print(res)


if __name__ == '__main__':
    ss = SendData()
    ss.post_xml(url_normal,'opt_new')