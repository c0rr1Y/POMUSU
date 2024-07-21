#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

def cmdline():
    parser = argparse.ArgumentParser(description="")
    target = parser.add_argument_group('Target')
    target.add_argument('-u',dest='url',type=str,help="Input your url target")
    target.add_argument('-f',dest='file',type=str,help="Input your target's file")
    fuzz = parser.add_argument_group('fuzz')
    fuzz.add_argument('-fuzz', dest='fuzz', action='store_true',default=False, help="Enable fuzzing mode")
    args = parser.parse_args()

    #args = argparse.Namespace(url=None, file='url2.txt', fuzz=False)
    #args = argparse.Namespace(url='http://192.168.6.166:8080/', file=None, fuzz=False)
    return args
if __name__ == '__main__':
    print(cmdline())


