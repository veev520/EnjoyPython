# -*- coding: utf-8 -*-
"""
如何使用特殊方法
"""


from math import hypot


class Vector:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Vector(%r, %r)' % (self.x, self.y)

    # def __str__(self):
    #     return 'Vector: (%r, %r)' % (self.x, self.y)

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        """
        尽管 Python 里有 bool 类型，但实际上任何对象都可以用于需要布尔值的上下文中（比如
        if 或 while 语句，或者 and、or 和 not 运算符）。为了判定一个值 x 为真还是为假，
        Python 会调用 bool(x)，这个函数只能返回 True 或者 False。

        默认情况下，我们自己定义的类的实例总被认为是真的，除非这个类对 __bool__ 或者
        __len__ 函数有自己的实现。bool(x) 的背后是调用 x.__bool__() 的结果；如果不存
        在 __bool__ 方法，那么 bool(x) 会尝试调用 x.__len__()。若返回 0，则 bool 会返回
        False；否则返回 True。

        我们对 __bool__ 的实现很简单，如果一个向量的模是 0，那么就返回 False，其他情况
        则返回 True。因为 __bool__ 函数的返回类型应该是布尔型，所以我们通过
        bool(abs(self)) 把模值变成了布尔值。
        """
        # return bool(abs(self))
        return bool(self.x or self.y)

    def __add__(self, other):
        """
        通过 __add__ 和 __mul__， 为向量类带来了 + 和 * 这两个算术运算符。
        值得注意的是，这两个方法的返回值都是新创建的向量对象，被操作的两个向量
        （self 或 other）还是原封不动，代码里只是读取了它们的值而已。

        中缀运算符的基本原则就是不
        改变操作对象，而是产出一个新的值。
        """
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)


if __name__ == '__main__':
    v1 = Vector(3, 4)
    v2 = Vector(1, 2)
    print('repr', v1)

    print('abs', abs(v1))
    print('bool', bool(v1))
    print('add', 'v1 + v2 = ', (v1 + v2))
    print('mul', 'v1 * 2 = ', v1 * 2)

    print()
    s = 'abcdefga'
    print('s: ', s)
    print('s中a 出现的次数', s.count('a'))
    print('s中b 出现的次数', s.count('b'))
