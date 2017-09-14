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

BASE_URL = 'http://aladd.net'
db = Database()
lock = threading.RLock()


class Link(db.Entity):
    url = PrimaryKey(str)
    # 0 等待爬, 1 爬完, 2 正在爬
    status = Required(int)


def init_db():
    db.bind(provider='sqlite', filename='aladd.sqlite', create_db=True)
    sql_debug(False)
    db.generate_mapping(create_tables=True)


@db_session
def put_sites(urls):
    for url in urls:
        site = Link.get(url=url)
        if not site:
            s = Link(url=url, status=0)


@db_session
def crawl_url(url):
    s = Link.get(url=url)
    if s:
        s.status = 1
        commit()


@db_session
def has(url):
    return Link.exists(url=url)


@db_session
def show(url):
    s = Link.get(url=url)
    if not s:
        print(None)
    else:
        print(s.url, s.is_crawled)


@db_session
def show_all():
    # for s in Site.select():
    #     print(s.url, s.is_crawled)
    for l in Link.select():
        print(l.url, l.status)


@db_session
def show_detail():
    all_count = Link.select().count()
    done_count = count(s for s in Link if s.status == 1)
    wait_count = count(s for s in Link if s.status == 0)
    prep_count = count(s for s in Link if s.status == 2)
    print('全部链接数\t', all_count)
    print('完成链接数\t', done_count)
    print('等待链接数\t', wait_count)


@db_session
def clean_prep():
    l = select(l for l in Link if l.status == 2)[:]
    for ll in l:
        ll.status = 0
    commit()


@db_session
def get_site(url):
    return Link.get(url=url)


@db_session
def get_url():
    u = select(s for s in Link if s.status == 0)[:1]
    if len(u):
        u[0].status = 2
        commit()
        return u[0].url
    return BASE_URL


def check_folder(path):
    """
    检查文件夹是否存在
    不存在则创建文件夹
    """
    if not os.path.isdir(path):
        os.mkdir(path)


def save_img(url, name, path='pic'):
    """
    保存图片
    :param url: 图片链接
    :param name: 图片名
    :param path: 保存的位置
    """
    path = 'E:/Veev/Pictures/爬虫专用/aladd/' + path
    check_folder(path)

    #  后缀
    suffix = '.jpg'
    if url.endswith('.png'):
        suffix = '.png'
    elif url.endswith('.gif'):
        suffix = '.gif'

    name = path + '/' + name + '_' + str(len(os.listdir(path)) + 1) + suffix
    r = requests.get(url=url, headers=header_helper.pc())
    if r.status_code == 200:
        open(name, 'wb').write(r.content)
    # request.urlretrieve(url, name)
    pass


def is_aladd(url):
    if re.match('http://aladd.net', url):
        return True
    else:
        return False


def is_archives(url):
    if re.match('http://aladd.net/archives/\d+.html', url):
        return True
    else:
        return False


def start_crawl(proxy, thread):
    print('start_crawl', proxy, thread)
    # proxy = proxy_helper.get(BASE_URL)
    # print(proxy)
    # if not proxy:
    #     return
    # proxy = {'http': 'http://183.66.64.120:3128', 'https': 'https://183.66.64.120:3128'}
    # proxy = {'http': 'http://180.175.141.220:53281', 'https': 'https://180.175.141.220:53281'}
    # proxy = {'http': 'http://221.4.133.67:53281', 'https': 'https://221.4.133.67:53281'}
    url = None
    lock.acquire()
    try:
        url = get_url()
    finally:
        # 释放锁:
        lock.release()
    # url = 'http://aladd.net/archives/30327.html'
    while True:
        if not url:
            lock.acquire()
            try:
                url = get_url()
            finally:
                # 释放锁:
                lock.release()
        try:
            print('正在抓取网页', url, thread)
            r = requests.get(url=url, headers=header_helper.pc(), proxies=proxy, timeout=30)
            if r.status_code == 200:
                # 这个网页抓取完了, 设置为已抓取
                crawl_url(url)

                soup = BeautifulSoup(r.text, 'lxml')
                # 拿到全部的内链
                a_list = soup.find_all('a', {'href': re.compile(BASE_URL)})
                site_list = list()
                for a in a_list:
                    _url = a['href']
                    if _url == BASE_URL:
                        continue
                    site_list.append(_url)
                put_sites(site_list)

                if is_archives(url):
                    archive_id = re.findall('\d+', url)[0]
                    title = soup.find_all('div', {'class': 'entry_title'})[0].h1.text
                    img_list = soup.find_all('a', {'href': url})
                    for img in img_list:
                        save_img(img.img['src'], img.img['alt'], path=(archive_id + '_' + title))
                    print('保存图片', title, len(img_list), thread)

                print('抓取完成, 本页链接数', len(site_list), thread)
        except Exception as e:
            print('====================')
            print('抓取异常', thread, e)
            print('====================')
        finally:
            time.sleep(random.randint(5, 12) * 0.1)
            lock.acquire()
            try:
                url = get_url()
            finally:
                # 释放锁:
                lock.release()
            pass
    pass


if __name__ == '__main__':
    init_db()
    # clean_prep()
    show_detail()
    # show_all()
    thread_list = list()
    p1 = {'http': 'http://183.66.64.120:3128', 'https': 'https://183.66.64.120:3128'}
    p2 = {'http': 'http://180.175.141.220:53281', 'https': 'https://180.175.141.220:53281'}
    p3 = {'http': 'http://221.4.133.67:53281', 'https': 'https://221.4.133.67:53281'}
    thread_list.append(threading.Thread(target=start_crawl, args=(p1, 'thread-1')))
    thread_list.append(threading.Thread(target=start_crawl, args=(p2, 'thread-2')))
    thread_list.append(threading.Thread(target=start_crawl, args=(p3, 'thread-3')))
    for t in thread_list:
        # t.start()
        pass
    pass