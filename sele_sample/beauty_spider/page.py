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
import re, time, threading

class Page():
    
    def __init__(self):
        # 下一步driver应用phantomjs
#         self.driver = webdriver.Firefox()
        self.driver = webdriver.PhantomJS(executable_path=r"C:\Python36\phantomjs.exe")
        self.wait = WebDriverWait(self.driver, 20)
        self.assist = Assistant()
    

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
        
    
    def navigate_to(self, element, way, sth):
        handle = self.driver.current_window_handle
        element.click()
        time.sleep(10)
        handles = self.driver.window_handles
        for newhandle in handles:
            if newhandle != handle:
                self.driver.switch_to_window(newhandle)
                self.wait_element(way, sth)
                self.get_element(way, sth).click()
                break
        # 去掉文件名中的特殊字符,举例如下
        # re.sub(r'[`~!@#$%^&*)(+=}{|><,.?/\\\-\]\[]', '', STRING)
        group = re.sub(
                    r'[`~!@#$%^&*)(+=}{|><,.?/\\\-\]\[]', 
                    '', 
                    self.get_element("XPATH", "//div[@class='article']/h2").text
                )
        self.assist.create_folder(group)
        print("【"+group+"】 ---组创建成功")
        images = self.get_elements("XPATH", "//div[@id='content']/img")
        
        '''下一步通过多线程或多进程加快图片下载'''
        for image in images:
#             self.assist.download_image(group, image.get_attribute('src'))
#             time.sleep(3)
            lock = threading.Condition()
            t = threading.Thread(target=self.assist.download_image, args=(lock, group, image.get_attribute('src')))
            t.start()
            t.join()
        
        self.driver.close()
        self.driver.switch_to_window(handle)
        
   
    def quit(self):
        self.driver.quit()
