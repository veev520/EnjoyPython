import requests
import re
import random


def main():
    is_archives = 'http://aladd.net/archives/\d+.html'
    url = 'http://aladd.net/archives/32.635.html'
    if re.match('http://aladd.net/archives/\d+.html', url):
        print(True)
    else:
        print(False)

    print(re.findall('fast_color', 'haha 90dsaflkj > fast_color safsadlfjlk'))
    fmt = '{:2}\t{:3}'
    print(fmt.format(1,2))


if __name__ == '__main__':
    main()
