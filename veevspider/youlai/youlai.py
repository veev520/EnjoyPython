#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pony.orm import *
import os
from bs4 import BeautifulSoup
import requests
import time
import threading
import re
import random
from base import header_helper, proxy_helper, log
import json

BASE_URL = 'http://www.youlai19.cn'


def get_show_by_id(id):
    proxy = {'http': '122.224.227.202:3128', 'https': '122.224.227.202:3128'}
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    url = BASE_URL + '/show.asp?id=' + str(id)
    try:
        r = requests.get(url=url, headers=header, proxies=proxy, timeout=30)
        if r.status_code == 200:
            r.encoding = 'GBK'
            yl = dict()
            soup = BeautifulSoup(r.text, 'lxml')
            yl['title'] = soup.find_all('h1', {'class': 'aTitle'})[0].text
            tt = soup.find_all('span', {'class': 'tt'})[0]
            a_list = tt.find_all('a')
            yl['category'] = [{'id': a['href'][a['href'].index('=') + 1:],
                               'category': a.text} for a in a_list[1:]]
            yl['detail'] = soup.find_all('div', {'class': 'luru_c'})[0].span.text
            content = soup.find('div', id='content')
            p_list = content.find_all('p')
            content_list = list()
            for p in p_list:
                if p.has_attr('style'):
                    content_list.append({'type': 'img',
                                         'url': p.img['src'],
                                         'desc': p.span.text})
                    pass
                else:
                    content_list.append({'type': 'text',
                                         'text': p.text})
                    pass
            yl['content'] = content_list
            # print(json.dumps(yl))
            # 写入 JSON 数据
            with open('yl/' + str(id) + '.json', 'w', encoding='utf-8') as f:
                json.dump(yl, f, ensure_ascii=False, indent=4)
            print('完成', id)
    except Exception as e:
        print('异常: get_show_by_id', id, e)
    pass


def parse_show(content):
    pass


if __name__ == '__main__':
    for i in range(1314, 2919):
        get_show_by_id(i)
        time.sleep(0.5)
    pass