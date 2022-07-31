# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import scrapy
from scrapy.pipelines.images import ImagesPipeline
from picture_spider.settings import IMAGES_STORE
import os
import hashlib


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # print(item['src'])
        yield scrapy.Request(url=item['src'], meta={'item': item})

    def item_completed(self, results, item, info):
        # image_path = [x['src'] for ok, x in results if ok]
        # if image_path:
        #     item['name'] = os.path.basename(image_path)
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta["item"]
        img_name =os.path.basename(item['src'])
        image_path = os.path.join(IMAGES_STORE, item['title'], img_name)
        if os.path.exists(image_path):
            md5 = hashlib.md5()
            md5.update(item['src'].encode("utf-8"))
            img_name = md5.hexdigest() + os.path.splitext(img_name)[-1]
            image_path = os.path.join(IMAGES_STORE, item['title'], img_name)
        # item['image_paths'] = image_path
        print(image_path)
        return image_path


class PictureSpiderPipeline(object):
    def process_item(self, item, spider):
        return item
