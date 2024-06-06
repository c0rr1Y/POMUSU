#!/usr/bin/env python
# -*- coding: utf-8 -*-


import random


Author = "admire@"

Banner = '''\033[1;31m
██████╗  ██████╗ ███╗   ███╗██╗   ██╗███████╗██╗   ██╗
██╔══██╗██╔═══██╗████╗ ████║██║   ██║██╔════╝██║   ██║
██████╔╝██║   ██║██╔████╔██║██║   ██║███████╗██║   ██║
██╔═══╝ ██║   ██║██║╚██╔╝██║██║   ██║╚════██║██║   ██║
██║     ╚██████╔╝██║ ╚═╝ ██║╚██████╔╝███████║╚██████╔╝
╚═╝      ╚═════╝ ╚═╝     ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝ 
                 \033[1;34m

    Author: {0}
                 
'''.format(Author)

# 设置线程数，默认30
threads = 60

ceye_rawurl = "8rrsa8.ceye.io"
ceye_token = "27c12e2c352d76a9fc1f48b2d1f08ab6"

ysoserial="D:\ctftools\ysoserial-all.jar"

user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/68.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) '
            'Gecko/20100101 Firefox/68.0',
            'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/68.0']

head = {
    "User-Agent": random.choice(user_agents)
}
