# -*- coding: utf-8 -*-

import os
import sqlite3
from sqlite3 import Error

data_name = "data.db"


def create_db():
    if not os.path.exists(data_name):
        open(data_name, "w")
    conn = connection()
    if conn is not None:
        create_search(conn)
        create_ad(conn)


def connection():
    conn = None
    try:
        conn = sqlite3.connect(data_name)
        conn.execute('PRAGMA foreign_keys = 1')
        return conn
    except Error as e:
        print(e)
    return conn


def create_search(co):
    data = co.cursor()
    create = """CREATE TABLE IF NOT EXISTS search (
            id              INTEGER         PRIMARY KEY     AUTOINCREMENT,
            web             VARCHAR(255)    NOT NULL,
            subject         VARCHAR(255)    NOT NULL,
            link_search     VARCHAR(255)    NOT NULL        UNIQUE,
            link_ad         VARCHAR(255)    NOT NULL
        )"""
    data.execute(create)


def create_ad(co):
    data = co.cursor()
    create = """CREATE TABLE IF NOT EXISTS ad (
            id          INTEGER         PRIMARY KEY     AUTOINCREMENT,
            site_id     INTEGER,
            title       VARCHAR(255)    NOT NULL,
            description VARCHAR(255)    NULL,
            location    VARCHAR(255)    NOT NULL,
            link        VARCHAR(255)    NOT NULL        UNIQUE,
            status      VARCHAR(255)    NOT NULL        DEFAULT'non_lu',
            
            CONSTRAINT fk_site_id FOREIGN KEY (site_id) REFERENCES search(id) ON DELETE CASCADE
        )"""
    data.execute(create)


def select(sql):
    try:
        conn = connection()
        c = conn.cursor()
        c.execute(sql)
        result = c.fetchall()
        return result
    except Error as e:
        print(e)
