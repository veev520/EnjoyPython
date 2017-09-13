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

    print(random.randint(5, 15) * 0.1)


if __name__ == '__main__':
    main()
