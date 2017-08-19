# -*- coding: utf-8 -*-
# @Time     : 2017/8/17 23:31
# @File     : downloader.py

import logging
import urllib.error
import urllib.request


def download(url):
    logging.log(logging.DEBUG, "download %s start", url)
    try:
        request = urllib.request.Request(url)
        respone = urllib.request.urlopen(request)
        content = respone.read()
        content = content.decode()
    except urllib.error.HTTPError as err:
        content = None
        logging.log(logging.INFO, "download %s raise:%s", url, err.msg)
    else:
        logging.log(logging.DEBUG, "download %s finished!", url)
    return content
