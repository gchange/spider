# -*- coding: utf-8 -*-
# @Time     : 2017/8/17 23:31
# @File     : downloader.py

import urllib.error
import urllib.request
import time


def download(url, delay=0):
    start = time.time()
    try:
        request = urllib.request.Request(url)
        respone = urllib.request.urlopen(request)
        content = respone.read()
        content = content.decode()
    except urllib.error.HTTPError as err:
        content = None
    end = time.time()
    delay = end - start + delay
    if delay > 0:
        time.sleep(end-start)
    return content
