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
    
               
    def navigate_and_download_image(self):
        elements = self.page.get_elements("XPATH", "//span[@class='title']/a")
        for element in elements:
            group_name = element.text
            sTime = time.time()
            print("【"+group_name+"】 ---正在下载中,请稍后...")
            self.page.navigate_to(element, "XPATH", "//em[@id='opic']")
            print("【"+group_name+"】耗时{}秒".format(time.time()-sTime)+"---下载完毕！")
        
        if self.page.driver.find_element_by_xpath("//a[@class='last']").is_displayed():
            next_page = self.page.driver.find_element_by_xpath("//a[@class='last']/preceding-sibling::a[1]")
        else:
            next_page = self.page.driver.find_element_by_xpath("//div[@class='page']/a")[-1]
             
        if next_page is not None:
            next_page.click()
            self.navigate_and_download_image()
            
    
    def teardown(self):
        self.page.quit()