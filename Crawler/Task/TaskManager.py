#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/21 11:24
# @Author  : HT
# @Site    : 
# @File    : TaskManager.py
# @Software: PyCharm Community Edition
# @Describe: Desc
# @Issues  : Issues


from Crawler.Task.TaskDownloader import TaskDownloader
from Crawler.Task.TaskUploader import TaskUploader
from Socket.SocketProtocol import *

class TaskManager(TaskDownloader, TaskUploader):
    def __init__(self):
        TaskDownloader.__init__(self)
        TaskUploader.__init__(self)

    def processing_task(self, task_info):
        task_id = task_info['task_id']
        data = None
        if task_id is None:
            return None
        if task_id == '1':
            data = self._download_task_1(task_info)
        elif task_id == '2':
            data = self._download_task_2(task_info)
        return data

    def upload_data(self, data, task_info, crawler):
        task_id = task_info['task_id']
        if task_id == '1':
            response = self._upload_task_1(data, task_info, crawler)
            return response
        elif task_id == '2':
            response = self._upload_task_2(data, task_info, crawler)
            return response
