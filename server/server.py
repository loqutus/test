#!/usr/bin/env python3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
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
def close_db():
    if hasattr(g, app.config['DATABASE']):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.route('/')
def index():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('index.html', entries=entries)

if __name__ == '__main__':
    app.run(port=app.config['LISTEN_PORT'], host=app.config['LISTEN_HOST'], debug=app.config['DEBUG'])
