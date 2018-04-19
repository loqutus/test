#!/usr/bin/env python3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import json
import sqlite3

app = Flask(__name__)
app.config.from_object('settings')
app.config.from_envvar('SETTINGS', silent=True)


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(arg):
    if hasattr(g, app.config['DATABASE']):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.route('/')
def index():
    try:
        db = get_db()
        cur = db.execute('select key, value from entries order by id desc')
        entries = cur.fetchall()
        return render_template('index.html', entries=entries)
    except Exception as e:
        return str(e), 500


@app.route('/add', methods=['POST'])
def add_entry():
    try:
        db = get_db()
        db.execute('insert into entries (key, value) values (?, ?)',
                   [request.json['key'], request.form['value']])
        db.commit()
        return 'OK', 200
    except Exception as e:
        return str(e), 500


@app.route('/initdb', methods=['GET'])
def initdb():
    try:
        init_db()
        return 'OK', 200
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run(port=app.config['LISTEN_PORT'], host=app.config['LISTEN_HOST'], debug=app.config['DEBUG'])
