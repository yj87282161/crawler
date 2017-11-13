#!/usr/bin/env python
# -*- encoding:utf-8 -*-
'''
Created on 2017-11-9

@author: Administrator
'''
from sele_sample.beauty_spider.robot import Robot
# import pdb

if __name__ == '__main__':
    robot = Robot("http://www.mmjpg.com")
    robot.setup('CLASS', 'pic')
    try:
        robot.download_image_groups()
        robot.navigate_to_next_page()
        # pdb.run('robot.navigate_and_download_image()')
    except Exception as e:
        print(e)
    finally:
        robot.teardown()