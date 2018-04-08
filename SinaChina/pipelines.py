# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from SinaChina.settings import BASE_PATH


class SinachinaPipeline(object):
    def process_item(self, item, spider):

        big_path = BASE_PATH + '/' + item['big_title']
        if not os.path.exists(big_path):
            os.mkdir(big_path)

        small_path = big_path + '/' + item['small_title']
        if not os.path.exists(small_path):
            os.mkdir(small_path)

        nav_path = small_path + '/' + item['nav_title']
        if not os.path.exists(nav_path):
            os.mkdir(nav_path)

        file = open(nav_path + '/' + item['title']+'.txt','w',encoding='utf-8')
        file.write(item['content'])
        file.close()

        return item
