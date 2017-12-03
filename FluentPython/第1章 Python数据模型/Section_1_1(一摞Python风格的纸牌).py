# -*- coding: utf-8 -*-
"""
一摞Python风格的纸牌
"""


import collections
from random import choice

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, item):
        return self._cards[item]


if __name__ == '__main__':
    card = Card('7', 'diamonds')
    print('定义一张卡牌', card)

    deck = FrenchDeck()
    # 调用的FrenchDeck 的 __len__ 方法
    print('长度', len(deck))

    # 调用的 FrenchDeck 的 __getitem__ 方法
    print('第一张卡牌', deck[0])
    print('最后一张卡牌', deck[-1])

    # 随机取一张卡牌
    print('随机一张卡牌', choice(deck))

    # 切片
    print('第4 到 6 张卡牌', deck[4:6])
    print('第5张开始, 每隔13张', deck[5::13])

    # 迭代
    for c in deck:
        print('迭代', end=': ')
        print(c, end=', ')
    print()
    for c in reversed(deck):
        print('反向迭代', end=': ')
        print(c, end=', ')
    print()

    # 由于没有实现 __contains__ in 实际上是迭代搜索
    print(card in deck)
    print(Card('666', 'club') in deck)

    # 排序
    suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)


    def spades_high(card):
        rank_value = FrenchDeck.ranks.index(card.rank)
        return rank_value * len(suit_values) + suit_values[card.suit]

    print('排序', end=': ')
    for card in sorted(deck, key=spades_high):
        print(card, end=', ')
    print()






