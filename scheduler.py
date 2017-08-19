# -*- coding: utf-8 -*-
# @Time     : 2017/8/18 0:01
# @File     : scheduler.py

from queue import Queue

import downloader
import page_parser
import save
from cache import DownloadCache
import logging


class Scheduler(object):
    def __init__(self, url, max_depth=None):
        self.link_queue = Queue()
        self.link_queue.put((url, 0))
        self.cache = DownloadCache(1000, 0.001)
        self.max_depth = max_depth

    def start(self):
        while not self.link_queue.empty():
            url, depth = self.link_queue.get()
            if self.max_depth is not None and depth > self.max_depth:
                logging.log(logging.DEBUG, "filter url:%s reach max depth!", url)
                continue
            if url in self.cache:
                logging.log(logging.DEBUG, "filter url:%s already download!", url)
                continue
            else:
                logging.log(logging.DEBUG, "download url:%s", url)
                self.cache.add(url)
            content = downloader.download(url, 2)
            save.save(url, content)
            links = page_parser.parser(content)
            urls = page_parser.link_parser(url, links)
            for url in urls:
                self.link_queue.put((url, depth+1))
        logging.log(logging.INFO, "Finished!!!")
