#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from kit.wordcloudkit.kit import WordCloudKit


def file_name(file_dir):

    root_list = []
    empty_dir = []
    file_list = []
    title_list = []
    for root, dirs, files in os.walk(file_dir):
        root_list.append(root)
        if not files:
            empty_dir.append(root)
        for file in files:
            file_list.append(file)
        title_list.append(root[29 + root[28:].find('_'):])
        # print(root)     # 当前目录路径
        # print(dirs)     # 当前路径下所有子目录
        # print(len(files))    # 当前路径下所有非目录子文件
    print('文件夹数量', len(root_list))
    print('文件数量', len(file_list))
    print('空文件夹', len(empty_dir))
    with open('../../test/data.txt', 'w', encoding='utf-8') as aladd_file:
        text = ' '.join(title_list)
        aladd_file.write(text)
        WordCloudKit().show(text)
    print('Done')


if __name__ == '__main__':
    file_name('E:/Veev/Pictures/爬虫专用/aladd/')
    pass