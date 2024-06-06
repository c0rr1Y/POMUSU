#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from config.data import Urls, logging

class initoptions:
    def __init__(self, args):
        self.key = ["\"","“","”","\\","'"]
        Urls.url = []
        self._url = args.url
        self._file = args.file
        self.fuzz= args.fuzz
        self.target()
    def target(self):
        if self._url:
            self.check(self._url)
        elif self._file:
            if os.path.exists(self._file):
                with open(self._file, 'r') as f:
                    for i in f:
                        self.check(i.strip())
            else:
                errMsg = "File {0} is not find".format(self._file)
                logging.error(errMsg)
                exit(0)

    def check(self, url):
        for key in self.key:
            if key in url:
                url = url.replace(key,"")
        if not url.startswith('http') and url:
            # 若没有http头默认同时添加上http与https到目标上
            Urls.url.append("http://" + str(url))
            Urls.url.append("https://" + str(url))
        elif url:
            Urls.url.append(url)

