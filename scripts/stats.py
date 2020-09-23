# -*- coding: utf-8 -*-

import database as db


def data_status():
    sql = """SELECT web FROM polls_search GROUP BY web"""
    results = db.db_select(sql)
    list_web = {}
    for result in results:
        list_web[result[0]] = {}
    list_status = {"not-read": 0, "applied": 0, "inadequate": 0, "expired": 0, "other": 0}
    for web in list_web:
        list_web[web].update(list_status)
    sql = """SELECT status, COUNT(status), polls_search.web FROM polls_ad
        LEFT JOIN polls_search ON polls_ad.site_id = polls_search.id
        GROUP BY status, polls_search.web"""
    results = db.db_select(sql)
    for result in results:
        list_web[result[2]][result[0]] = result[1]
    conn = db.db_connection()
    for data in list_web:
        total = list_web[data]["not-read"] + list_web[data]["applied"] + list_web[data]["inadequate"] + list_web[data]["expired"] + list_web[data]["other"]
        sql = """INSERT INTO polls_stat (web, not_read, applied, inadequate, expired, other, total)
                VALUES ('{}', {}, {}, {}, {}, {}, {})"""\
        .format(data, list_web[data]["not-read"], list_web[data]["applied"], list_web[data]["inadequate"], list_web[data]["expired"], list_web[data]["other"], total)
        insert = db.injection_sql(conn, sql)
        if insert == "update":
            sql = """UPDATE polls_stat SET not_read={}, applied={}, inadequate={}, expired={}, other={}, total={}
                    WHERE web = '{}'"""\
                .format(list_web[data]["not-read"], list_web[data]["applied"], list_web[data]["inadequate"], list_web[data]["expired"], list_web[data]["other"], total, data)
            db.injection_sql(conn, sql)
    db.db_close(conn)


if __name__ == '__main__':
    data_status()
