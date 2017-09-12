#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jieba


seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
print("Full Mode: " + "/".join(seg_list))  # 全模式

# In[15]:

seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
print("Precise Mode: " + "/".join(seg_list))  # 精确模式，默认状态下也是精确模式

# In[16]:

seg_list = jieba.cut("他来到网易杭研大厦。")
print("Default Mode: " + "/".join(seg_list))

# In[14]:

seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造。")  # 搜索引擎模式
print("Search Mode: " + "/".join(seg_list))


if __name__ == '__main__':
    pass