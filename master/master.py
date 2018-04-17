#!/usr/bin/env python3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from .. import common

app = Flask(__name__)
app.config.from_object('master_settings')
app.config.from_envvar('MASTER_SETTINGS', silent=True)

if __name__ == '__main__':
    app.run(port=app.config['LISTEN_PORT'], host=app.config['LISTEN_HOST'], debug=app.config['DEBUG'])
