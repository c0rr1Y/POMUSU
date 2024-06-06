#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json

from config.color import color
from urllib.parse import urlsplit
from config.data import logging
from lib.match import match

from config.data import File

class Identify:
    def __init__(self):
        File.file=[]
        self.poc = match()
        filepath = os.path.abspath('library/POMUSU.json')
        with open(filepath, 'r', encoding='utf-8') as file:
            finger = json.load(file)

            for name, value in finger.items():
                self.obj = value
    def display_status(self):
        status = self.datas['status']
        if status == 200:
            return color.green(self.datas['status'])
        else:
            return color.yellow(self.datas['status'])
    def run(self, datas):
        self.datas = datas
        cms = self._has_app()
        self.datas["cms"] = ','.join(set(cms))
        if cms:
            xpoc = self.poc.poc(self.datas["url"], self.datas['cms'])
            if len(xpoc)==1:
                xpoc.append(f"{cms}未发现漏洞")

            results = {"url": self.datas["url"], "cms": self.datas["cms"], "title": self.datas["title"],
                       "status": self.datas["status"], "Server": self.datas['Server'], "vul": xpoc
                       }
            File.file.append(results)
            Msg = "{0} {1} {2} {4} {3}\n{5}".format(color.green(self.datas['cms']),
                                                    color.blue(self.datas['Server']), self.datas['title'],
                                                    self.display_status(), self.datas["url"], color.red(xpoc))

            logging.success(Msg)
        else:
            Msg = "{0} {1} {2} {4} {3}".format(color.green(self.datas['cms']),
                                               color.blue(self.datas['Server']), self.datas['title'],
                                               self.display_status(), self.datas["url"])
            logging.success(Msg)

    def _has_app(self):
        cms = []
        for line in self.obj:
            flag = 1
            if line['method'] == "faviconhash" and str(self.datas["faviconhash"]) == line["keyword"][0]:
                cms.append(line["cms"])
            elif line["method"] == "keyword":
                for key in line["keyword"]:
                    if key not in str(self.datas[line["location"]]):
                        flag = 0
                if flag == 1:
                    cms.append(line["cms"])
            else:
                pass
        return cms
