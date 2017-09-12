#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pony.orm import *

db = Database()


class Site(db.Entity):
    url = PrimaryKey(str)


def main():
    db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
    sql_debug(False)
    db.generate_mapping(create_tables=True)
    init_data()
    show()


def init_data():
    put_all(str(x) for x in range(100, 200))


@db_session
def put(url):
    if not has(url):
        s = Site(url=url)


@db_session
def put_all(urls):
    for url in urls:
        if not has(url):
            s = Site(url=url)


@db_session
def has(url):
    return Site.exists(url=url)


@db_session
def show():
    s = select(s for s in Site)
    for n in s:
        print(n.url)


if __name__ == '__main__':
    main()
