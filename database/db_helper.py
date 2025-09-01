import sqlite3
from flask import g, current_app

def _connect():
    con = sqlite3.connect(current_app.config["DATABASE_PATH"])
    con.row_factory = sqlite3.Row
    return con

def get_db():
    if "db" not in g:
        g.db = _connect()
    return g.db

def query_all(sql: str, params: tuple = ()):
    cur = get_db().execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    return rows

def query_one(sql: str, params: tuple = ()):
    cur = get_db().execute(sql, params)
    row = cur.fetchone()
    cur.close()
    return row

def execute(sql: str, params: tuple = ()):
    db = get_db()
    db.execute(sql, params)
    db.commit()
