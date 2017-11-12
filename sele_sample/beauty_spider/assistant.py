#!/usr/bin/env python
# -*- encoding:utf-8 -*-
'''
Created on 2017-11-10

@author: Administrator
'''
import os
import requests

class Assistant():
    
    def __init__(self):
        self.image_root_folder = r"D:\workspace\imooc\sele_sample\images"
        
    
    def create_folder(self, filename):
        if filename is None:
            return
        # 判断当前self.image_root_folder是否为文件夹
        if not os.path.isdir(self.image_root_folder):
            # 创建images父文件夹(D:\workspace\imooc\beauty_spider\images)
            os.mkdir(self.image_root_folder)
        # images父文件夹与新文件夹名组成子文件夹路径
        image_folder = os.path.join(self.image_root_folder, filename)
        # 判断当前image_folder是否为文件夹
        if not os.path.isdir(image_folder):
            # 创建各图片组子文件夹(D:\workspace\imooc\beauty_spider\images\魂牵梦绕的清纯妹子月夕Lily)
            os.mkdir(image_folder)
            
        return image_folder
    
    
    def download_image(self, lock, group, image_url):
        lock.acquire()
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
            print(image_url+"---下载完成")
        except Exception as e:
            print(e)
        lock.release()
        