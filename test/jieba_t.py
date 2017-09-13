#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jieba


text = '''
九天大陆，天穹之上有九条星河，每一条星河，都由无尽星辰交织而成，这九条星河，又称九重天。
'''
seg_list = jieba.cut(text, cut_all=True)
# print("Full Mode: " + "/".join(seg_list))  # 全模式
dic = dict()
for s in seg_list:
    if s:
        if s in dic:
            dic[s] = dic[s] + 1
        else:
            dic[s] = 1
d2 = sorted(dic.items(), key=lambda d: d[1], reverse=True)
print(d2)

# In[15]:

seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
print("Precise Mode: " + "/".join(seg_list))  # 精确模式，默认状态下也是精确模式

# # In[16]:
#
# seg_list = jieba.cut("他来到网易杭研大厦。")
# print("Default Mode: " + "/".join(seg_list))
#
# # In[14]:
#
# seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造。")  # 搜索引擎模式
# print("Search Mode: " + "/".join(seg_list))


if __name__ == '__main__':
    pass