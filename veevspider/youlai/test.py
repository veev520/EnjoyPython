#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Veev'

import json
import os


def get_category():
    d = dict()
    for root, dirs, files in os.walk('yl'):
        for f in files:
            # 读取数据
            with open('yl/' + f, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for i in range(0, len(data['category'])):
                    d[data['category'][i]['id']] = {
                        'id': data['category'][i]['id'],
                        'category': data['category'][i]['category']
                    }
                    if i == 0:
                        d[data['category'][i]['id']]['father'] = '0'
                    else:
                        d[data['category'][i]['id']]['father'] = data['category'][i - 1]['id']

    l = list()
    for dd in d:
        l.append(d[dd])
        l = sorted(l, key=lambda x: int(x['id']))
    print(l)
    # 写入 JSON 数据
    with open('category.json', 'w', encoding='utf-8') as f:
        json.dump(l, f, ensure_ascii=False, indent=4)
    pass


if __name__ == '__main__':
    # 读取数据
    with open('category.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for d in data:
            if d['father'] == '8':
                print(d)
        print(data)