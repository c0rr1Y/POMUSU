#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from vul.thinkphp import thinkphp
from vul.jindie import jindie
from vul.weblogic import weblogic
from vul.springboot import springboot
from vul.shiro import shiro
from vul.tongda import tongda
class match:
    def __int__(self):
        pass
    def poc(self,args1,args2):
        self.url = args1
        self.cms = args2
        vulnerabilities = [
            '致远',
            '金蝶',
            '蓝凌',
            '用友',
            'Shiro',
            'Weblogic',
            'spring-boot',
            '华天动力',
            'ThinkPHP',
            '通达'
        ]
        counter = 0
        for i in vulnerabilities:
            counter += 1
            pattern = i
            matches = re.findall(pattern, self.cms)
            if matches:
                if counter==1:
                    return
                elif counter==2:
                    self.vul = jindie()
                    return self.vul.ALL(self.url)
                elif counter==3:
                    return
                elif counter == 4:
                    return
                elif counter == 5:
                    self.vul= shiro()
                    return self.vul.ALL(self.url)
                elif counter == 6:
                    self.vul = weblogic()
                    return self.vul.ALL(self.url)
                elif counter == 7:
                    self.vul = springboot()
                    return self.vul.ALL(self.url)
                elif counter == 8:
                    return
                elif counter == 9:
                    self.vul=thinkphp()
                    return self.vul.ALL(self.url)
                elif counter == 10:
                    self.vul=tongda()
                    return self.vul.ALL(self.url)


            else:
                continue
        return "No vulnerabilities found"
if __name__ == '__main__':
    url='http://43.143.165.217:8080/'
    cms='ThinkPHP'
    ob=match()
    list=ob.poc(url,cms)
    print(list)

