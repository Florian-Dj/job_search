# -*- coding: utf-8 -*-

import time
import main
import database
import requests


def home():
    sql = """SELECT * FROM site GROUP BY web"""
    results = database.select(sql)
    for result in results:
        # parse(result[3])
        print(result)
    time.sleep(2)
    main.main()
