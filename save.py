# -*- coding: utf-8 -*-
# @Time     : 2017/8/19 17:50
# @File     : save.py

import hashlib
import os


def save(url, content):
    name = hashlib.md5(url.encode('utf-8')).hexdigest()
    root = "./data"
    if not os.path.exists(root):
        os.makedirs(root)
    with open("./data/%s.html" % name, 'w') as f:
        f.write(content)
