### 1.3 特殊方法一览

> Python 语言参考手册中的[“Data Model”](https://docs.python.org/3/reference/datamodel.html)一章列出了 83 个特殊方法的名字，其中 47 个用于实现算术运算、位运算和比较操作。

##### 表1-1: 跟运算符无关的特殊方法

| 类别        | 方法名    |  
| --------    | ------    |
| 字符串/字节序列表示形式 | \_\_repr__ 、 \_\_str__ 、 \_\_format__ 、 \_\_bytes__      |
| 数值转换        | \_\_abs__ 、 \_\_bool__ 、 \_\_complex__ 、 \_\_int__ 、 \_\_float__ 、 \_\_hash__ 、 \_\_index__      |
| 集合模拟        | \_\_len__ 、 \_\_getitem__ 、 \_\_setitem__ 、 \_\_delitem__ 、 \_\_contains__      |
