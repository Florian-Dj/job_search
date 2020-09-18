# -*- coding: utf-8 -*-

import sqlite3
from sqlite3 import Error


def injection_sql(conn, sql):
    try:
        data = conn.cursor()
        data.execute(sql)
    except conn.IntegrityError:
        return "update"
    except conn.Error as e:
        print(e)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("../data.db")
        conn.execute('PRAGMA foreign_keys = 1')
        return conn
    except Error as e:
        print(e)
    return conn


def db_close(conn):
    try:
        conn.commit()
        conn.close()
    except conn.Error as e:
        print(e)


def db_select(sql):
    try:
        conn = db_connection()
        c = conn.cursor()
        c.execute(sql)
        result = c.fetchall()
        return result
    except Error as e:
        print(e)