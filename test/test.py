from functools import wraps


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
    foo()
    pass


if __name__ == '__main__':
    main()
