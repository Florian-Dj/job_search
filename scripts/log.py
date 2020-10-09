# -*- coding: utf-8 -*-

import logging


def log_sql():
    logging.basicConfig(
        filename='../logs/jobs_cron.log',
        level=logging.INFO,
        format='%(name)s %(asctime)s %(levelname)s %(pathname)s %(message)s',
        datefmt='%m/%d/%y %X'
    )
    return logging


def log_ads():
    logging.basicConfig(
        filename='../logs/jobs_ads.log',
        level=logging.ERROR,
        format='%(name)s %(asctime)s %(levelname)s %(pathname)s %(message)s',
        datefmt='%m/%d/%y %X'
    )
    return logging
