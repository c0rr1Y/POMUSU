#!/usr/bin/env python
# -*- coding: utf-8 -*-


import queue
import threading
import requests
import urllib3
from colorama import Fore
from config import config
from config.data import Urls
urllib3.disable_warnings()
def exploit(ip, q, total_tasks,progress):

    while not q.empty():
        exp_list = q.get()
        for n in exp_list:
            if ''.join(ip)[-1] == '/':
                URL=''.join(ip) + n
            else:
                URL =''.join(ip) + '/' + n
            try:
                response = requests.get(URL)
                if response.status_code == 200:
                    print(Fore.GREEN + "目录存在 -> {}".format(URL))
            except requests.RequestException as e:
                pass
        with progress['lock']:
            progress['completed'] += 1
            completed = progress['completed']
            print(f"\r完成率: {completed}/{total_tasks} ({(completed / total_tasks) * 100:.2f}%)", end='')
        q.task_done()

class DirSearch:
    def __init__(self):
        # 初始化队列
        self.total_tasks = None
        self.q = queue.Queue(maxsize=0)
        self.load_dict()
        progress = {
            'completed': 0,
            'lock': threading.Lock()
        }
        threads = []
        for num in range(config.threads):
            t = threading.Thread(target=exploit, args=(set(Urls.url), self.q,self.total_tasks,progress))
            t.start()
            threads.append(t)
        # 等待所有任务完成
        self.q.join()
        # 等待所有线程完成
        for t in threads:
            t.join()
        print("扫描完成")

    def load_dict(self):
        """
        加载字典文件，并将其分块放入队列
        """
        dict_list = []
        with open('library/dicc.txt', "r", encoding="utf-8") as dict_file:
            for line in dict_file:
                dict_list.append(line.strip())

        # 将字典分块，每个块包含 30 个路径
        chunk_size = 30
        list = [dict_list[i:i + chunk_size] for i in range(0, len(dict_list), chunk_size)]
        for index in range(len(list)):
            self.q.put(list[index])
        self.total_tasks = len(list)



