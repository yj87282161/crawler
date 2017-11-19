#!/usr/bin/env python
# -*- encoding:utf-8 -*-
'''
Created on 2017-11-10

@author: Administrator
'''
from sele_sample.beauty_spider.page import Page
import time, re

class Robot():
    
    def __init__(self, url):
        self.url = url
        self.page = Page()
        # self.image_group_num = 1
        self.page_num = 1
        self.total_page = None
        
    
    def setup(self, way, sth):
        try:
            print('...启动浏览器...')
            self.page.launch_browser(self.url)
            print('...等待页面加载中...')
            self.page.wait_element(way, sth)
            self.total_page = re.findall('\d+', self.page.get_element("CLASS", "info").text)[0]
            print('...共有图片{}页'.format(self.total_page))
        except:
            print('...重试,请稍等...')
            self.page.quit()
            self.setup(way, sth)
    
              
    def download_image_groups(self):
        elements = self.page.get_elements("XPATH", "//span[@class='title']/a")
        print('...当前第{}页'.format(self.page_num))
        for element in elements:
            print("="*20)
            self.page.download_image_into_root(element)
            # print(element.text)
            # self.page.download_image_into_group(element, image_group_num)
            # self.image_group_num += 1
        self.page_num += 1
             
    def navigate_to_next_page(self):
        print('...上一页所有图片组下载完成,下一页准备中...')
        # 获取最后一个子节点
        next_page = self.page.driver.find_element_by_xpath("//div[@class='page']/*[last()]")
        # 如最后一个子节点文本为"最旧",获取倒数第二个节点
        if(next_page.text == "最旧"):
            next_page = self.page.driver.find_element_by_xpath("//div[@class='page']/*[last()-1]")
        
        if next_page.text == str(self.total_page):
            print('======所有图片已下载完成======')
            return
        else:
            print('...准备进入{}:第{}页...'.format(next_page.text, self.page_num))
            next_page.click()
            time.sleep(3)
            self.download_image_groups()
            self.navigate_to_next_page()
#    next_page = self.page.driver.find_element_by_xpath("//a[@class='last']/preceding-sibling::a[1]")
#    next_page = self.page.driver.find_elements_by_xpath("//div[@class='page']/a")[-1]

            
    def teardown(self):
        self.page.quit()