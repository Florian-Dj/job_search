# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import scrape, database as db
import log

list_id_expired = []


def select_ads():
    sql = """SELECT polls_ad.id, polls_ad.link, polls_search.web  FROM polls_ad
        LEFT JOIN polls_search ON polls_ad.site_id = polls_search.id
        WHERE status='not-read'"""
    results = db.db_select(sql)
    if results:
        for result in results:
            if result[2] == "Linkedin":
                analysis_lk(result[1], result[0])
            elif result[2] == "Pole-Emploi":
                analysis_pe(result[1], result[0])
        update_sql()


def analysis_lk(url, id_ad):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    ads = soup.find('figcaption', class_="closed-job__flavor--closed")
    if ads:
        list_id_expired.append(id_ad)


def analysis_pe(url, id_ad):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    ads = soup.find('meta', content='Offre non disponible')
    if ads:
        list_id_expired.append(id_ad)


def update_sql():
    conn = db.db_connection()
    for id_ad in list_id_expired:
        sql = """UPDATE polls_ad SET status='expired' WHERE id={}""".format(id_ad)
        db.injection_sql(conn, sql)
    db.db_close(conn)


if __name__ == '__main__':
    logging = log.log_sql()
    logging.info("Run script analysis")
    select_ads()
    logging.info("Finish script analysis")
