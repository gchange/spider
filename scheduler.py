# -*- coding: utf-8 -*-
# @Time     : 2017/8/18 0:01
# @File     : scheduler.py

import logging
import threading
import time
from itertools import cycle
from queue import Empty
from queue import Queue

import downloader
import page_parser
import save
from cache import DownloadCache


class Worker(threading.Thread):
    def __init__(self, delay, feedback):
        super(Worker, self).__init__()
        self.work_queue = Queue()
        self.delay = delay
        self.feedback = feedback

    def run(self):
        logging.log(logging.INFO, "worker %s work on!", self.getName())
        while True:
            try:
                job = self.work_queue.get()
                if job is None:
                    break
                start = time.time()
                self.do_work(*job)
                end = time.time()
                delay = end - start + self.delay
                if delay > 0:
                    time.sleep(delay)
            except:
                pass
        logging.log(logging.INFO, "worker %s off work!", self.getName())

    def do_work(self, depth, url):
        content = downloader.download(url)
        links = page_parser.parser(content)
        urls = page_parser.link_parser(url, links)
        self.feedback(depth + 1, urls)
        save.save(url, content)

    def add_job(self, item):
        self.work_queue.put(item)


class Scheduler(object):
    def __init__(self, url, max_depth=None, delay=0, worker_num=1):
        self.feedback_queue = Queue()
        self.feedback_queue.put((0, url))
        self.cache = DownloadCache(1000, 0.001)
        self.max_depth = max_depth

        self.worker_num = worker_num
        workers = [Worker(delay, self.feedback) for _ in range(worker_num)]
        for worker in workers:
            worker.start()
        self.workers = cycle(workers)

    def start(self):
        logging.log(logging.INFO, "Scheduler start!")
        while True:
            try:
                depth, url = self.feedback_queue.get(timeout=30)
                worker = next(self.workers)
                worker.add_job((depth, url))
            except Empty:
                break
        for _ in range(self.worker_num):
            worker = next(self.workers)
            worker.add_job((None, None))
        logging.log(logging.INFO, "Scheduler done!")

    def is_need_download(self, depth, url):
        if self.max_depth is not None and depth > self.max_depth:
            logging.log(logging.DEBUG, "filter url:%s reach max depth!", url)
            return False

        if url in self.cache:
            logging.log(logging.DEBUG, "filter url:%s already download!", url)
            return False

        self.cache.add(url)
        return True

    def feedback(self, depth, urls):
        for url in urls:
            if not self.is_need_download(depth, url):
                continue
            self.feedback_queue.put((depth, url))
