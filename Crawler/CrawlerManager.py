#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/21 13:54
# @Author  : HT
# @Site    : 
# @File    : CrawlerManager.py
# @Software: PyCharm Community Edition
# @Describe: Desc
# @Issues  : Issues

import sys
import os
import json
import time

from Crawler.BaseCrawler import *
from threading import Thread
from Crawler.Task.TaskManager import TaskManager as tk

class CrawlerManager(BaseCrawler, Thread):
    def __init__(self):
        BaseCrawler.__init__(self, 'crawler.log')
        Thread.__init__(self)
        self.task_manager = tk()
        self.threads = list()

    def crawl(self):
        task = self.application_task()
        task_num = task['task_nums']
        items = task['items']
        if int(task_num) == 0 or items is None or len(items) == 0:
            self.logger.debug('没有需要处理的任务')
        else:
            data = self.task_manager.processing_task(task)
            if data is None:
                self.logger.error('get date error for task:{}'.format(task))
            else:
                response = self.task_manager.upload_data(data, task, self)
                self.logger.debug('upload result :{}'.format(response))

    def application_task(self):
        time = datetime_to_timestamp(get_datestr())
        parm = {pc.MSG_TYPE: pc.APPLICATION_TASKS, pc.CLIENT_ID: self.clientId, pc.REQUEST_TIME: time}
        response = self.socketClient.send(json.dumps(parm))
        response_dict = json.loads(response)
        error = response_dict.get(pc.ERROR)
        if error :
            self.logger.error('application task error:%s'%(response_dict))
            return None
        else:
            # self.task_manager.processing_task(response_dict)
            return response_dict

    def process_crawl_scheduler(self):
        while True:
            for thread in self.threads:
                if thread.isAlive() is not True:
                    self.threads.remove(thread)
            self.logger.debug('current threads num:%s'%(len(self.threads)))
            if len(self.threads) >= 5:
                time.sleep(5)
                continue
            try:
                t = Thread(target=self.crawl, name='application tasks')
                t.setDaemon(True)
                self.threads.append(t)
                t.start()
                time.sleep(5)
            except Exception as error:
                self.logger.error('create thread error:{}'.format(error))
                time.sleep(5)

    def run(self):
        BaseCrawler.actionCrawler(self)
        self.process_crawl_scheduler()


if __name__ == '__main__':
    am = CrawlerManager()

    am.setDaemon(True)
    am.start()
    am.join()