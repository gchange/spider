# -*- coding: utf-8 -*-
# @Time     : 2017/8/19 8:51
# @File     : page_parser.py

import urllib.parse

from bs4 import BeautifulSoup


def parser(content):
    soup = BeautifulSoup(content)
    links = set()
    for tag in soup.find_all('a'):
        try:
            link = tag['href']
        except KeyError:
            pass
        else:
            links.add(link)
    return links


def link_parser(url, links):
    urls = set()
    root = urllib.parse.urlparse(url)
    for link in links:
        link_parser = urllib.parse.urlparse(link)
        if not link_parser.netloc and not link_parser.path:
            continue

        scheme = link_parser.scheme or root.scheme
        netloc = link_parser.netloc or root.netloc
        url = urllib.parse.urlunparse(
                (scheme, netloc, link_parser.path, link_parser.params, link_parser.query, link_parser.fragment))
        urls.add(url)
    return urls
