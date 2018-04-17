import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object('master_settings')
app.config.from_envvar('MASTER_SETTINGS')

