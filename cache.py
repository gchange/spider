# -*- coding: utf-8 -*-
# @Time     : 2017/8/19 17:34
# @File     : cache.py

from pybloom import BloomFilter


class DownloadCache(object):
    def __init__(self, capacity, error_rate):
        self.cache = BloomFilter(capacity=capacity, error_rate=error_rate)

    def add(self, url):
        self.cache.add(url)

    def __contains__(self, item):
        return item in self.cache
