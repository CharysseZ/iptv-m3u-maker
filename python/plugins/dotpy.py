#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tools
import time
import re
import db
import threading
from.threads import ThreadPool
import requests


class Source(object):

    def __init__(self):
        self.T = tools.Tools()
        self.now = int(time.time() * 1000)

    def getSource(self):
        sourceFilePath = '/srv/iptv/python/plugins/dotpy_source'
        all_lines = []
        network_addresses = []
        with open(sourceFilePath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                network_addresses.append(line.strip())

        threads = ThreadPool(20)
        for address in network_addresses:
            response = requests.get(address)
            if response.status_code == 200:
                lines = response.text.splitlines()
                all_lines.extend(lines)
            else:
                print(f"Failed to fetch data from {address}. Status code: {response.status_code}")

        total = len(all_lines)
        for i in range(0, total):
            line = all_lines[i].strip()
            item = line.split(',', 1)
            threads.add_task(self.detectData, title=item[0], url=item[1])

        threads.wait_completion()

    def detectData(self, title, url):
        print('detectData', title, url)
        info = self.T.fmtTitle(title)

        netstat = self.T.chkPlayable(url)

        if netstat > 0:
            cros = 1 if self.T.chkCros(url) else 0
            data = {
                'title': str(info['id']) if info['id']!= '' else str(info['title']),
                'url': str(url),
                'quality': str(info['quality']),
                'delay': netstat,
                'level': info['level'],
                'cros': cros,
                'online': 1,
                'udTime': self.now,
            }
            self.addData(data)
            self.T.logger('正在分析[ %s ]: %s' % (str(info['id']) + str(info['title']), url))
        else:
            pass  # MAYBE later :P

    def addData(self, data):
        DB = db.DataBase()
        sql = "SELECT * FROM %s WHERE url = '%s'" % (DB.table, data['url'])
        result = DB.query(sql)

        if len(result) == 0:
            data['enable'] = 1
            DB.insert(data)
        else:
            id = result[0][0]
            DB.edit(id, data)
