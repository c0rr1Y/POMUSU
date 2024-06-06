#!/usr/bin/env python
# -*- coding: utf-8 -*-
import queue
import threading
from venv import logger

import requests
import random
import codecs
import mmh3

from urllib.parse import urlsplit, urljoin



from config.data import Urls,Urlerror
from config import config
from lib.identify import Identify
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()



class Request:
    def __init__(self):
        self.checkcms = Identify()
        q = queue.Queue(maxsize=0)
        chunk_size = 20
        chunks = [Urls.url[i:i + chunk_size] for i in range(0, len(Urls.url), chunk_size)]
        for chunk in chunks:
            q.put(chunk)
            # 启动线程
        threads = []
        for num in range(config.threads):
            t = threading.Thread(target=self.apply, args=(q,))
            t.start()
            threads.append(t)

        # 等待所有任务完成
        q.join()

        # 等待所有线程完成
        for t in threads:
            t.join()

    def apply(self, q):
        while not q.empty():
            exp_list = q.get()
            for url in exp_list:
                try:
                    #proxies = { "http": "127.0.0.1:8080","https": "127.0.0.1:8080"}
                    with requests.get(url, timeout=10, headers=self.get_headers(), cookies=self.get_cookies(), verify=False,
                                      allow_redirects=True, stream=True) as response:
                        if int(response.headers.get("content-length", default=1000)) > 100000:
                            self.response(url, response, True)
                        else:
                            self.response(url, response)
                except KeyboardInterrupt:
                    logger.error("用户强制程序，系统中止!")
                    exit(0)
                except Exception as e:
                    pass
            q.task_done()

    def response(self, url, response, ignore=False):
        if ignore:
            html = ""
            size = response.headers.get("content-length", default=1000)
        else:
            response.encoding = response.apparent_encoding if response.encoding == 'ISO-8859-1' else response.encoding
            response.encoding = "utf-8" if response.encoding is None else response.encoding
            html = response.content.decode(response.encoding,"ignore")
            size = len(response.text)
        title = self.get_title(html).strip().replace('\r', '').replace('\n', '')
        status = response.status_code
        server = response.headers["Server"] if "Server" in response.headers else ""
        server = "" if len(server) > 50 else server
        faviconhash = self.get_faviconhash(url)

        datas = {"url": url, "title": title, "body": html, "status": status, "Server": server, "size": size,
                 "header": response.headers, "faviconhash": faviconhash}
        self.checkcms.run(datas)

    def get_faviconhash(self, url):
        try:
            parsed = urlsplit(url)
            url = urljoin(parsed.scheme + "://" + parsed.netloc, "favicon.ico")
            response = requests.get(url, headers=self.get_headers(), timeout=4)
            favicon = codecs.encode(response.content, "base64")
            hash = mmh3.hash(favicon)
            return hash
        except:
            return 0

    def get_title(self, html):
        soup = BeautifulSoup(html, 'lxml')
        title = soup.title
        if title and title.text:
            return title.text
        if soup.h1:
            return soup.h1.text
        if soup.h2:
            return soup.h2.text
        if soup.h3:
            return soup.h3.text
        desc = soup.find('meta', attrs={'name': 'description'})
        if desc:
            return desc['content']

        word = soup.find('meta', attrs={'name': 'keywords'})
        if word:
            return word['content']

        text = soup.text
        if len(text) <= 200:
            return text
        return ''

    def get_headers(self):
        """
        生成伪造请求头
        """
        ua = random.choice(config.user_agents)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,'
                      'application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': ua,
        }
        return headers

    def get_cookies(self):
        cookies = {'rememberMe': 'test'}
        return cookies

