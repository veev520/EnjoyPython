from functools import wraps
import re


class LogIt(object):
    def __init__(self, print_time=False):
        self.p = print_time
    pass

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            import time
            if self.p:
                print(time.ctime(), f.__name__ + '() was called')
            else:
                print(f.__name__ + '() was called')
            return f(*args, **kwargs)
        return wrap


def hi(print_time=False):
    def hi_decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            import time
            if print_time:
                print(time.ctime(), f.__name__ + '() was called')
            else:
                print(f.__name__ + '() was called')
            return f(*args, **kwargs)
        return wrap
    return hi_decorator


@LogIt(print_time=0)
def foo():
    print('我是一个方法')


def main():
    # foo()
    # for i in range(1, 2):
    #     print(i)
    #     if i > 50:
    #         print('{0:2} > 3'.format(i))
    #         break
    # else:
    #     print('没有中断')

    s = 'qwe001qwe'
    print(re.search('\d{2,}', s))
    pass


if __name__ == '__main__':
    main()
