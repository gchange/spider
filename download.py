# -*- coding: utf-8 -*-
# @Time     : 2017/8/13 11:48
# @File     : download.py


import re
import urllib.error
import urllib.parse
import urllib.request


def download(url):
    print('Downloading %s' % url)
    try:
        html = urllib.request.urlopen(url).read()
        html = html.decode()
    except urllib.error.URLError as err:
        html = None
        print('Download error!', err)
    return html


def crawl_sitemap(url):
    print('Crawling %s' % url)
    # 测试时http://example.webscraping.com/sitemap.xml下载到的并不是sitemap格式的，自己制作了一份代替
    # sitemap = download(url)
    with open("sitemap.xml", "r") as f:
        sitemap = f.read()
    if sitemap is None:
        print('Download sitemap error!')
        return

    links = re.findall('<loc>(.*?)</loc>', sitemap)
    print('Start download %d pages' % len(links))
    for link in links:
        download(link)


def crawl_id():
    id = 1
    while id < 20:
        url = "http://example.webscraping.com/view/-%d" % id
        download(url)
        id += 1


def link_crawler(seed_url, link_regex):
    """Crawl from the given seed URL following links matched by link_regex
    """
    crawl_queue = [seed_url]
    seen = {seed_url}
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        # filter for links matching our regular expression
        for link in get_links(html):
            if re.match(link_regex, link):
                link = urllib.parse.urljoin(seed_url, link)
                if link in seen:
                    continue
                crawl_queue.append(link)


def get_links(html):
    """Return a list of links from html
    """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)


if __name__ == '__main__':
    # url = b'http://example.webscraping.com/sitemap.xml'
    # crawl_sitemap(url)

    # crawl_id()

    seed_url = "http://example.webscraping.com"
    link_regex = "/places/default/(index|view)"
    link_crawler(seed_url, link_regex)
