"""
get user info from weibo by uid
"""

import json
import os
import re
import time
from datetime import datetime
import random

import requests
from bs4 import BeautifulSoup
from logger import StreamLogger

from rich.progress import track


def insert_cookies():
    with open('./cookies') as f:
        for line in f:
            cookie_str = line.replace('\n', '')
            return cookie_str


def get_json(self, params):
    """获取网页中json数据"""
    url = "https://m.weibo.cn/api/container/getIndex?"
    StreamLogger.info("请求url: %s", url)
    r = requests.get(url, params=params, headers=self.headers, verify=False)
    return r.json(), r.status_code


if __name__ == '__main__':
    StreamLogger.info("Start to get user info from weibo by uid")
    # 读取uid
    uid_list = []
    with open("./test_uid.txt", "r", encoding="utf-8") as f:
        for line in f:
            uid_list.append(line.strip())
    headers = {

        "User_Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/110.0.0.0 Safari/537.36",
        "cookie": insert_cookies(),
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0",
    }

    # 发起请求 request
    StreamLogger.info("Start to request...")
    for uid in track(uid_list[:1]):
        time.sleep(random.randint(3, 10))
        params = {"containerid": "100505" + str(uid)}
        url = "https://m.weibo.cn/api/container/getIndex?"
        rep = requests.get(url, params=params, headers=headers, verify=False)
        print(url)
        rep_json = rep.json()

        # beautifulsoup
        # format json
        print(json.dumps(rep_json, indent=4, ensure_ascii=False))
        # rep_json to dict
        dic = dict(rep_json['data']['userInfo'])
        # 是否认证
        print(dic['verified'])
        # 认证类型
        print(dic['verified_type_ext'])
        # 认证信息
        print(dic['verified_reason'])
        print(dic)
    # 获取用户信息
    StreamLogger.info("Start to get user info...")
    user_info_list = []