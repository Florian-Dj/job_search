# -*- coding: utf-8 -*-

import logging


def log_conf():
    logging.basicConfig(
        filename='jobs_django.log',
        level=logging.INFO,
        format='%(name)s %(asctime)s %(levelname)s %(pathname)s %(message)s',
        datefmt='%m/%d/%y %X'
    )
    return logging
