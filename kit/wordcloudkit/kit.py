#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import jieba
import numpy as np
from PIL import Image


def list_count(lis):
    dic = dict()
    for s in lis:
        if s:
            if s in dic:
                dic[s] = dic[s] + 1
            else:
                dic[s] = 1
    d2 = sorted(dic.items(), key=lambda d: d[1], reverse=True)
    print(d2)
    return d2


class WordCloudKit(object):
    def __init__(self):
        pass

    def show(self, text):
        # 通过 jieba 分词进行分词并通过空格分隔
        word_list = jieba.cut(text, cut_all=True)
        wl_space_split = " ".join(word_list)
        wc = WordCloud(
            background_color='black',  # 设置背景颜色
            mask=mask_img,  # 设置背景图片
            max_words=150,  # 设置最大现实的字数
            stopwords=STOPWORDS,  # 设置停用词
            font_path='C:/Windows/Fonts/simsun.ttc',  # 设置字体格式，如不设置显示不了中文
            max_font_size=100,  # 设置字体最大值
            random_state=30,  # 设置有多少种随机生成状态，即有多少种配色方案
            # scale=1,
            width=1400,
            height=1400
        ).generate(wl_space_split)
        # 根据图片生成词云颜色
        image_colors = ImageColorGenerator(mask_img)
        # wc.recolor(color_func=image_colors)                     # 采用图片颜色

        # 以下代码显示图片
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        # wc.to_file('word_cloud.jpg')
        pass


# 读入背景图片
mask_img = np.array(Image.open("D:\WorkSpace\Python\EnjoyPython\image\img2html\img.jpg"))

# 读取要生成词云的文件
text_file = open('D:\WorkSpace\Python\EnjoyPython\kit\wordcloudkit\data.txt', encoding='utf-8').read()


if __name__ == '__main__':
    WordCloudKit().show(text_file)
    pass