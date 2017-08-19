# -*- coding: utf-8 -*-
# @Time     : 2017/8/17 23:46
# @File     : main.py

import scheduler
import logging

logging.basicConfig(level=logging.DEBUG)
url = "http://example.webscraping.com/"
scheduler.Scheduler(url, 1, 2).start()
