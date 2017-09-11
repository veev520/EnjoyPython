import jieba


def main():
    seg_list = jieba.cut("全模式，把句子中所有的可以成词的词语都扫描出来, 速度非常快，但是不能解决歧义；", cut_all=True)
    print("Full Mode: " + "/ ".join(seg_list))  # 全模式


if __name__ == '__main__':
    main()
