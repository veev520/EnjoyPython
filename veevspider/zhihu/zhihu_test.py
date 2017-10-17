#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import lxml
import re
import requests

BASE = 'https://www.zhihu.com'


def get_zhihu(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    cookie = {
        "d_c0": "ACDC-lMDowuPTo4Rs3bxwI9TqlXywOCna2c=|1492698178",
        "_zap": "4b71a3f4-9f32-4de9-ae3b-36e421d4dfee",
        "_ga": "GA1.2.317945799.1492698169",
        "r_cap_id": "NWI3MDM3YWJjZDE1NGNjODg1MjZiMWYzNTdjZDY2NjY=|1505174357|44848f478c33f3e200726bae528f1ad2376bb6b3",
        "cap_id": "YWRlMzU3MTllOGRjNDc1OWI5MzVhNTE5YzA4MWQ2MDA=|1505174357|f11effccbaa734947b969d108a9096833a68c2ea",
        "z_c0": "Mi4xbTE5OUFnQUFBQUFBSU1MNlV3T2pDeGNBQUFCaEFsVk5FTExlV1FEMTRCU2RaQ25tVlN3UVRMdTRBalZDZUhjU0l3|1505174800|69be593bb78b51fec809455e556c33b7f3570112",
        "q_c1": "ff782fd6d41b458fbb82606c9d9eddcb|1505174813000|1492237852000",
        "__utma": "51854390.317945799.1492698169.1505451283.1507109881.17",
        "__utmz": "51854390.1507109881.17.10.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/",
        "__utmv": "51854390.100--|2=registration_date=20160117=1^3=entry_date=20160117=1",
        "_xsrf": "a1e20ba9-f1a9-4295-84e1-4622dd0b86f5"
    }
    r = requests.get(url, headers=header, cookies=cookie)
    soup = BeautifulSoup(r.text, 'lxml')
    data = soup.find('div', id='data')
    ff = re.findall(r'"[a-z0-9\-]*":{"isFollowed"', str(data))
    for x in ff:
        id = x[1: x.index(':') - 1]
        print(id)
    pass


if __name__ == '__main__':
    get_zhihu(BASE + '/people/sgai/followers?page=2')
