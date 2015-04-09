#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File Name : 1.py
'''Purpose : Intro sth                                 '''
# Creation Date : 1428389717
# Last Modified :
# Release By : Doom.zhou


from flask import Flask, render_template, g
from flaskext.markdown import Markdown
import sqlite3
import os.path


DATABASE = 'example.db'
DEBUG = True
SECRET_KEY = 'NWUwZT@5YzQ5NzgzNzA3%'

app = Flask(__name__)
app.config.from_object(__name__)
Markdown(app)


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
    results = query_db("select * from entries order by updated desc limit 20")
    return render_template('index.html', results=results)


@app.route('/papers')
def papers():
    results = query_db("select * from papers order by updated desc limit 5")
    return render_template('papers.html', results=results)


@app.route('/papers/<id>')
def paper(id):
    results = query_db("select * from papers where id=%s" % id)
    return render_template('paper.html', results=results)
@app.route('/vuls')
def vuls():
    results = query_db("select * from entries where id=3")
    return render_template('vuls.html', results=results)


@app.route('/whitehats')
def whitehats():
    results = query_db("select * from entries where id=4")
    return render_template('whitehats.html', results=results)


@app.route('/tools')
def tools():
    results = query_db("select * from entries where id=5")
    return render_template('tools.html', results=results)


if __name__ == '__main__':
    app.run()
