#!/usr/bin/env python
# -*- encoding:utf-8 -*-
'''
Created on 2017-11-10
@author: Administrator
'''
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from sele_sample.beauty_spider.assistant import Assistant
import re, time

class Page():
    
    def __init__(self):
        # 下一步driver应用phantomjs
#         self.driver = webdriver.Firefox()
        self.driver = webdriver.PhantomJS(executable_path=r"C:\Python36\phantomjs.exe")
        self.wait = WebDriverWait(self.driver, 20)
        self.assist = Assistant()
        # 设置当前标签为活动标签
        self.handle = self.driver.current_window_handle
    

    def launch_browser(self, url):
        self.driver.get(url)

        
    def wait_element(self, way, sth):
        if way == 'ID':
            self.wait.until(EC.presence_of_element_located((By.ID, sth)), "ERROR:ELEMENT NOT FOUND")
        elif way == 'TAG':
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, sth)), "ERROR:ELEMENT NOT FOUND")
        elif way == 'CLASS':
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, sth)), "ERROR:ELEMENT NOT FOUND")
        elif way == 'CSS':
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, sth)), "ERROR:ELEMENT NOT FOUND")
        elif way == 'NAME':
            self.wait.until(EC.presence_of_element_located((By.NAME, sth)), "ERROR:ELEMENT NOT FOUND")
        elif way == 'XPATH':
            self.wait.until(EC.presence_of_element_located((By.XPATH, sth)), "ERROR:ELEMENT NOT FOUND")
        else:
            self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, sth)), "ERROR:ELEMENT NOT FOUND")
    
    
    def get_element(self, way, sth):
        if way == 'ID':
            element = self.driver.find_element_by_id(sth)
        elif way == 'TAG':
            element = self.driver.find_element_by_tag_name(sth)
        elif way == 'CLASS':
            element = self.driver.find_element_by_class_name(sth)
        elif way == 'CSS':
            element = self.driver.find_element_by_css_selector(sth)
        elif way == 'NAME':
            element = self.driver.find_element_by_name(sth)
        elif way == 'XPATH':
            element = self.driver.find_element_by_xpath(sth)
        else:
            element = self.driver.find_element_by_link_text(sth)
        return element
    
    
    def get_elements(self, way, sth):
        if way == 'ID':
            elements = self.driver.find_elements_by_id(sth)
        elif way == 'TAG':
            elements = self.driver.find_elements_by_tag_name(sth)
        elif way == 'CLASS':
            elements = self.driver.find_elements_by_class_name(sth)
        elif way == 'CSS':
            elements = self.driver.find_elements_by_css_selector(sth)
        elif way == 'NAME':
            elements = self.driver.find_elements_by_name(sth)
        elif way == 'XPATH':
            elements = self.driver.find_elements_by_xpath(sth)
        else:
            elements = self.driver.find_elements_by_link_text(sth)
        return elements
        
    
    def click_element(self, element):
        element.click()
    
    
    def navigate_to_new_tab(self, handles, element):
        for newhandle in handles:
            if newhandle != self.handle:
                self.driver.switch_to_window(newhandle)
                try:
                    self.get_element("XPATH", "//em[@id='opic']").click()
                except:
                    self._back_to_image_groups()
                    self._navigate_to_images(element)
                break
    
    
    def _navigate_to_images(self, element):
        self.click_element(element)
        time.sleep(2)
        # 获取当前浏览器所有标签
        handles = self.driver.window_handles
        # 标签数为1时重新点击
        while len(handles) == 1:
            self.click_element(element)
        # 标签数为2进入新标签    
        self.navigate_to_new_tab(handles, element)
        
        
    def _back_to_image_groups(self):
        self.driver.close()
        self.driver.switch_to_window(self.handle)
    
    
    def download_image_into_group(self, element, image_group_num):
        self._navigate_to_images(element)
        # 去掉文件名中的特殊字符,举例如下
        # re.sub(r'[`~!@#$%^&*)(+=}{|><,.?/\\\-\]\[]', '', STRING)
        group = re.sub(
                    r'[`~!@#$%^&*)(+=}{|><,.?/\\\-\]\[]', 
                    '', 
                    self.get_element("XPATH", "//div[@class='article']/h2").text
                )
        group = '{}_'.format(str(image_group_num))+group
        self.assist.create_image_group_folder(group)
        print("...【"+group+"】 ---组创建成功")
        image_urls = [image.get_attribute('src') for image in self.get_elements("XPATH", "//div[@id='content']/img")]
            
        '''多线程加快图片下载'''
        self.assist.process_download_image(image_urls, group)
        
        self._back_to_image_groups()
        
    
    def download_image_into_root(self, element):
        self._navigate_to_images(element)
        # 去掉文件名中的特殊字符,举例如下
        # re.sub(r'[`~!@#$%^&*)(+=}{|><,.?/\\\-\]\[]', '', STRING)
        group = re.sub(
                    r'[`~!@#$%^&*)(+=}{|><,.?/\\\-\]\[]', 
                    '', 
                    self.get_element("XPATH", "//div[@class='article']/h2").text
                )
        # 创建文件夹
        self.assist.create_root_folder()
        image_urls = [image.get_attribute('src') for image in self.get_elements("XPATH", "//div[@id='content']/img")]
        '''多线程加快图片下载'''
        self.assist.process_download_image(image_urls, group)
        self._back_to_image_groups()
    
    
    def quit(self):
        self.driver.quit()
