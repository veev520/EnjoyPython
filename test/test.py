import requests
import re


def main():
    is_archives = 'http://aladd.net/archives/\d+.html'
    url = 'http://aladd.net/archives/32635.html'
    if re.match('http://aladd.net/archives/\d+.html', url):
        print(True)
    else:
        print(False)


if __name__ == '__main__':
    main()
    a= list()
    print(a)
