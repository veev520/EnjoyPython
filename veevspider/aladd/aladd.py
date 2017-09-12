from pony.orm import *
import os
from bs4 import BeautifulSoup
import requests
import time
import threading
import re
from base import header_helper, proxy_helper, log

BASE_URL = 'http://aladd.net'
db = Database()


class Site(db.Entity):
    url = PrimaryKey(str)
    is_crawled = Required(bool)


def init_db():
    db.bind(provider='sqlite', filename='aladd.sqlite', create_db=True)
    sql_debug(False)
    db.generate_mapping(create_tables=True)


@db_session
def put_sites(urls):
    for url in urls:
        site = Site.get(url=url)
        if not site:
            s = Site(url=url, is_crawled=False)


@db_session
def crawl_url(url):
    s = Site.get(url=url)
    if s:
        s.is_crawled = True
        commit()


@db_session
def has(url):
    return Site.exists(url=url)


@db_session
def show(url):
    s = Site.get(url=url)
    if not s:
        print(None)
    else:
        print(s.url, s.is_crawled)


@db_session
def show_all():
    for s in Site.select():
        print(s.url, s.is_crawled)


@db_session
def get_site(url):
    return Site.get(url=url)


@db_session
def get_url():
    u = select(s for s in Site if s.is_crawled == False)[:1]
    if len(u):
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
    check_folder(path)

    #  后缀
    suffix = '.jpg'
    if url.endswith('.png'):
        suffix = '.png'
    elif url.endswith('.gif'):
        suffix = '.gif'

    name = path + '/' + name + '_' + str(len(os.listdir('pic')) + 1) + suffix
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


def start():
    # proxy = proxy_helper.get(BASE_URL)
    # print(proxy)
    # if not proxy:
    #     return
    proxy = {'http': 'http://183.66.64.120:3128', 'https': 'https://183.66.64.120:3128'}
    try:
        url = get_url()
        url = 'http://aladd.net/archives/31671.html'
        print('正在抓取网页', url)
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
                site_list.append(_url)
                print(a)
            put_sites(site_list)

            print()
            print('===========================')
            print(is_archives(url))

            if is_archives(url):
                title = soup.find_all('div', {'class': 'entry_title'})[0].h1.text
                print('title', title)
                img_list = soup.find_all('img', {'alt': title})
                print('img_list', img_list)
                for img in img_list:
                    save_img(img['src'], title, path=title)
                    print(img)
    except Exception as e:
        print(e)
    finally:
        pass
    pass


if __name__ == '__main__':
    init_db()
    start()
    # show_all()