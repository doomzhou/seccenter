#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File Name : 1.py
'''Purpose : Intro sth                                 '''
# Creation Date : 1428389717
# Last Modified :
# Release By : Doom.zhou


import requests
import re
import bs4
import sqlite3
from urllib.parse import urlsplit
import os
from datetime import datetime


def connect_db():
    """Returns a new connection to the sqlite database"""
    return sqlite3.connect(
            'example.db', detect_types=sqlite3.PARSE_DECLTYPES
            )


def init_db():
    if not os.path.isfile('example.db'):
        f = open('schema.sql', 'r').read()
        db = connect_db()
        db.cursor().executescript(f)
        db.commit()


def load_vul():
    urls = [{'name': 'wooyun',
            'url': 'http://wooyun.org/bugs/new_submit/page/2'},
            {'name': 'loudong',
            'url': 'http://loudong.360.cn/vul/list/page/1'},
            {'name': 'vulbox',
            'url': 'https://www.vulbox.com/board/internet/page/1'}
            ]
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Archlinux) " + "Apple\
        WebKit537.36 (KHTML, like Gecko) Mozilla/5.0 (X11; " + "Linux\
        x86_64;rv:35.0)Gecko/20100101 Firefox/35.0'
    }
    pattern = re.compile('.*平安.*', re.I)
    entries = []
    for i in urls:
        url = i['url']
        domain = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
        r = requests.get(url, headers=headers)
        result = pattern.findall(r.text)
        if len(pattern.findall(r.text)) != 0:
            for j in result:
                soup = bs4.BeautifulSoup(str(j))
                for k in soup.select('a'):
                    url = k.attrs.get('href')
                    text = k.string
                    source = i['name']
                    entries.append({
                        'link': "%s%s" % (domain, url),
                        'title': text,
                        'source': source}
                        )

    for entry in entries:
        try:
            init_db()
            db = connect_db()
            db.cursor().execute(
                'INSERT INTO entries VALUES (?, ?, ?, ?, ?, ?, ?)', (
                    None,
                    entry['link'],
                    "http://127.0.0.1:5000/static/cog.png",
                    entry['title'],
                    entry['source'],
                    datetime.now(),
                    datetime.now()
                )
            )
            db.commit()
            db.close()
        except Exception as e:
            print(e)
            pass

if __name__ == "__main__":
    load_vul()
