# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests
import os


def check_folder(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def save_img(url, name, path='pic', use_index=False):
    """
    保存图片
    :param url: 图片链接
    :param name: 图片名
    :param path: 保存的位置
    :param use_index: 是否使用序号, 按照当前路径文件数量自增
    """
    check_folder(path)
    if use_index:
        name = str(len(os.listdir('pic')) + 1)

    # 后缀
    suffix = '.jpg'
    if url.endswith('.png'):
        suffix = '.png'
    elif url.endswith('.gif'):
        suffix = '.gif'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    name = path + '/' + name + suffix
    r = requests.get(url=url, headers=headers)
    if r.status_code == 200:
        open(name, 'wb').write(r.content)
    # request.urlretrieve(url, name)
    pass


class FirstPipeline(object):

    def process_item(self, item, spider):
        save_img(item['url'], item['name'], use_index=True)
    pass

