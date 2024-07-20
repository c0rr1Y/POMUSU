#!/usr/bin/env python
# -*- coding: utf-8 -*-


from config import config

from config.data import File
from lib.output import output
from lib.cmdline import cmdline
from lib.req import Request
from colorama import init as wininit
from lib.options import initoptions
from lib.dirsearch import DirSearch
wininit(autoreset=True)
if __name__ == '__main__':
    # 打印logo
    print(config.Banner)
    # 加载参数
    options = initoptions(cmdline())
    if options.fuzz:
        fuzz = DirSearch()
    else:
        run = Request()
        save=output()














