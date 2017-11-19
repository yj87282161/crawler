#!/usr/bin/env python
# -*- encoding:utf-8 -*-
'''
Created on 2017-11-10

@author: Administrator
'''
import os
import requests
from queue import Queue
import threading
import time

class Assistant():
    
    def __init__(self):
        self.image_root_folder = r"D:\workspace\imooc\sele_sample\images"
        self.queue = Queue() # 创建待下载url队列
        self.lock = threading.RLock()
        
    
    def create_root_folder(self):
        # 判断当前self.image_root_folder是否为文件夹
        if not os.path.isdir(self.image_root_folder):
            # 创建images父文件夹(D:\workspace\imooc\beauty_spider\images)
            os.mkdir(self.image_root_folder)

    
    def create_image_group_folder(self, filename):
        if filename is None:
            return
        self.create_root_folder()
        # images父文件夹与新文件夹名组成子文件夹路径
        image_folder = os.path.join(self.image_root_folder, filename)
        # 判断当前image_folder是否为文件夹
        if not os.path.isdir(image_folder):
            # 创建各图片组子文件夹(D:\workspace\imooc\beauty_spider\images\魂牵梦绕的清纯妹子月夕Lily)
            os.mkdir(image_folder)
        return image_folder
    
    
    def _download_image_into_group_folder(self, lock, group, image_url):
        with lock: # lock.acquire()        
            headers = {
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding':'gzip, deflate, sdch',
                    'Accept-Language':'zh-CN,zh;q=0.8',
                    'Cache-Control':'max-age=0',
                    'Connection':'keep-alive',
                    'Host':'img.mmjpg.com', # host不使用也可以，但是如果用，要用正确
                    'Referer':'http://img.mmjpg.com/{}'.format(str(image_url).split('/')[-2]), # 判断上一级地址，此网站防爬虫方式就是以此为判断依据的
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                }# 网站有反爬原因,添加请求头
            name = str(image_url).split('/')[-1] # re.split('/', image_url)[-1]
            full_name = self.image_root_folder + "\\" + group + "\\" + name
            try:
                r = requests.get(image_url, headers = headers)
                with open(full_name, 'wb') as f:
                    f.write(r.content)
            except Exception as e:
                print(e)
            
    
    def _download_image_into_root_folder(self, lock, group, image_url):
        with lock:        
            headers = {
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding':'gzip, deflate, sdch',
                    'Accept-Language':'zh-CN,zh;q=0.8',
                    'Cache-Control':'max-age=0',
                    'Connection':'keep-alive',
                    'Host':'img.mmjpg.com', # host不使用也可以，但是如果用，要用正确
                    'Referer':'http://img.mmjpg.com/{}'.format(str(image_url).split('/')[-2]), # 判断上一级地址，此网站防爬虫方式就是以此为判断依据的
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                }# 网站有反爬原因,添加请求头
            name = str(image_url).split('/')[-1]
            full_name = self.image_root_folder + "\\" + group + name
            try:
                r = requests.get(image_url, headers = headers)
                with open(full_name, 'wb') as f:
                    f.write(r.content)
            except Exception as e:
                print(e)
            # print("The {} is finished...".format(threading.current_thread().name))
    
    
    def _download_thread(self):
        while True:
            current_group, current_url = self.queue.get()
            self._download_image_into_root_folder(self.lock, current_group, current_url)
            # self._download_image_into_group_folder(self.lock, current_group, current_url)
            self.queue.task_done()
    
    def process_download_image(self, image_urls, group):
        sTime = time.time()
        
        for url in image_urls:
            self.queue.put((group,url))
            
        l = len(image_urls)    
    
        print("***【"+group+"】 ---正在下载中,请稍后...")
        while l:
            t = threading.Thread(target=self._download_thread) # , args=(group, image_url))
            t.daemon = True
            t.start()
            l -= 1
        self.queue.join()
        print("***【"+group+"】耗时{:.3f}秒".format(time.time()-sTime)+"---下载完毕！")
        