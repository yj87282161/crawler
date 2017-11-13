#!/usr/bin/env python
# -*- encoding:utf-8 -*-
'''
Created on 2017-11-10

@author: Administrator
'''
from sele_sample.beauty_spider.page import Page
import time

class Robot():
    
    def __init__(self, url):
        self.url = url
        self.page = Page()
        
    
    def setup(self, way, sth):
        try:
            self.page.launch_browser(self.url)
            self.page.wait_element(way, sth)
        except:
            self.page.quit()
            self.setup(way, sth)
    
              
    def download_image_groups(self):
        elements = self.page.get_elements("XPATH", "//span[@class='title']/a")
        for element in elements:
            group_name = element.text
            sTime = time.time()
            print("【"+group_name+"】 ---正在下载中,请稍后...")
            self.page.navigate_to(element, "XPATH", "//em[@id='opic']")
            print("【"+group_name+"】耗时{}秒".format(time.time()-sTime)+"---下载完毕！")
        
             
    def navigate_to_next_page(self):
        try:
            next_page = self.page.driver.find_element_by_xpath("//a[@class='last']/preceding-sibling::a[1]")
        except:
            next_page = self.page.driver.find_elements_by_xpath("//div[@class='page']/a")[-1]
            FLAG = 0
        finally:
            next_page.click()
            self.download_image_groups()
            if FLAG == 0:
                print('======所有图片已下载完成======')
                return
            else:
                self.navigate_to_next_page()
            
    def teardown(self):
        self.page.quit()