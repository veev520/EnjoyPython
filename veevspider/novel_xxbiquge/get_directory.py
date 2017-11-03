#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import lxml
from bs4 import BeautifulSoup
import re
import os
import time
import json

BASE_URL = 'http://www.xxbiquge.com'
BASE_PATH = 'F:/爬虫专用/小说/'


def check_folder(path):
    """
    检查文件夹是否存在
    不存在则创建文件夹
    """
    if not os.path.isdir(path):
        os.mkdir(path)


def has_file(file):
    return os.path.isfile(file)


def write_json(path, file_name, content):
    check_folder(BASE_PATH + path)
    with open(BASE_PATH + path + '/' + file_name + '.json', 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)


def put_novel_2_index(_id, title):
    check_folder(BASE_PATH)
    file_name = BASE_PATH + '_index.json'
    d = None
    if os.path.isfile(file_name):
        with open(BASE_PATH + '_index.json', 'r', encoding='utf-8') as f:
            d = json.load(f)
    else:
        d = dict()
    with open(BASE_PATH + '_index.json', 'w', encoding='utf-8') as f:
        d[_id] = title
        json.dump(d, f, ensure_ascii=False, indent=4)


def get_novel_form_index(_id):
    check_folder(BASE_PATH)
    file_name = BASE_PATH + '_index.json'
    if os.path.isfile(file_name):
        with open(BASE_PATH + '_index.json', 'r', encoding='utf-8') as f:
            d = json.load(f)
    else:
        return None
    title = d.get(_id)
    print(title)
    return title if title else None


def get_list(novel_id):
    """
    获取章节列表
    :param novel_id:
    """
    url = BASE_URL + '/' + str(novel_id) + '/'
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    r = requests.get(url, headers=header)
    if r.status_code == 200:
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')
        info = soup.find('div', id='info')
        # 标题
        title = info.h1.text
        novel = dict()
        novel['title'] = title
        # 作者, 格式    作   {若干空格}者：{中文冒号}某某某
        author = re.search('：\S+$', info.p.text)
        if author:
            novel['author'] = author.group()[1:]
        dd_list = soup.find_all('dd')
        sections = list()
        for dd in dd_list:
            a = dd.a
            sections.append({'section': a.text, 'url': a['href']})
        novel['sections'] = sections
        print(novel)
        put_novel_2_index(novel_id, title)
        write_json(title, '_index', novel)
    pass


def get_sections(novel_id):
    """
    爬取小说章节
    :param novel_id:
    :return:
    """
    title = get_novel_form_index(novel_id)
    if not title:
        print("Don 's has novel " + novel_id)
        return
    index_file = BASE_PATH + title + '/_index.json'
    if not has_file(index_file):
        print("Don 's has _index.json")
        return
    sections = None
    with open(index_file, 'r', encoding='utf-8') as f:
        d = json.load(f)
        sections = d['sections']

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    index = 0
    for section in sections:
        index += 1
        url = BASE_URL + section['url']
        try:
            r = requests.get(url, headers=header)
            if r.status_code == 200:
                r.encoding = 'utf-8'
                soup = BeautifulSoup(r.text, 'lxml')
                content = soup.find('div', id='content')
                bookname = soup.find_all('div', {'class': 'bookname'})[0].h1.text
                print(bookname)
                with open(BASE_PATH + title + '/' + '{:0>4}'.format(index) + '_' + bookname + '.txt', 'w+', encoding='utf-8') as f:
                    # 便于排序, 开头用 0001表示第一个文件
                    f.write(bookname)
                    f.write('\n\n')
                    f.write(str(content).replace('<br/><br/>', '\r\n').replace('<div id="content">', '').replace('</div>', ''))
                time.sleep(1)
        except Exception as e:
            print(e)
            continue
    pass


def create_novel(novel_id):
    """
    生成小说
    :param novel_id:
    """
    name = get_novel_form_index(novel_id)
    path = BASE_PATH + name
    novel_path = path + '/' + name + '.txt'
    print(novel_path)
    novel_list = []
    for f in os.listdir(path):
        if re.match('\d{4}', str(f)):
            novel_list.append(f)
    n1 = sorted(novel_list, key=lambda d: d[0:4], reverse=False)
    for n in n1:
        with open(path + '/' + n, 'r', encoding='utf-8') as novel_content:
            with open(novel_path, 'a', encoding='utf-8') as novel_file:
                novel_file.write(novel_content.read() + '\n\n')
    pass


if __name__ == '__main__':
    # get_list('10_10929')
    # get_list('74_74821')
    get_sections('10_10929')
    # create_novel('10_10929')
    pass
