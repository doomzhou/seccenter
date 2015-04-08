#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File Name : 1.py
'''Purpose : Intro sth                                 '''
# Creation Date : 1428389717
# Last Modified :
# Release By : Doom.zhou


from flask import Flask, render_template, g
import sqlite3
import os.path
import feedparser
from datetime import datetime


DATABASE = 'example.db'
DEBUG = True
SECRET_KEY = 'NWUwZT@5YzQ5NzgzNzA3%'

app = Flask(__name__)
app.config.from_object(__name__)


@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    return value.strftime(format)


def connect_db():
    """Returns a new connection to the sqlite database"""
    return sqlite3.connect(
            app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES
            )


def init_db():
    """Create the database if it doesn't exist"""
    if not os.path.isfile(app.config['DATABASE']):
        app.logger.debug('DB disappeared, making a new one')
        f = app.open_resource('schema.sql')
        db = connect_db()
        db.cursor().executescript(f.read().decode('utf-8'))
        db.commit()


def query_db(query, args=(), one=False):
    """Query database returning dictionary"""
    cur = g.db.execute(query, args)
    rv = [dict(
        (cur.description[idx][0], value)
        for idx, value in enumerate(row)) for row in cur.fetchall()
        ]
    return (rv[0] if rv else None) if one else rv


def populate_database():
    init_db()
    if data_is_stale():
        load_github()


def data_is_stale():
    """Find the last entry in the sqlite database to determine if we need to
    refresh the data.  This stops us from pulling them each request"""
    try:
        last_updated = g.db.cursor().execute(
                'select last_refresh from entries\
                        order by last_refresh desc limit 1'
                ).fetchone()[0]
    except:
        return True

    if not last_updated or (datetime.now() - last_updated).seconds > 10800:
        return True

    return False


def load_github():
    github = feedparser.parse("http://github.com/doomzhou.atom")
    g.db.cursor().execute('DELETE FROM entries WHERE source = "github"')

    for entry in github.entries:
        g.db.cursor().execute(
            'INSERT INTO entries VALUES (?, ?, ?, ?, ?, ?, ?)', (
                None,
                entry['link'],
                "http://127.0.0.1:5000/static/cog.png",
                entry['title'],
                "github",
                datetime.strptime(entry['updated'][:-1], '%Y-%m-%dT%H:%M:%S'),
                datetime.now()
            )
        )
    g.db.commit()


@app.before_request
def before_request():
    init_db()
    g.db = connect_db()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/')
def index():
    populate_database()
    results = query_db("select * from entries order by updated desc")
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run()
