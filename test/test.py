import requests
import re
import random


def main():
    is_archives = 'http://aladd.net/archives/\d+.html'
    url = 'http://aladd.net/archives/32635.html'
    if re.match('http://aladd.net/archives/\d+.html', url):
        print(True)
    else:
        print(False)

    print('http://aladd.net/archives/32635.html' == url)


if __name__ == '__main__':
    main()
