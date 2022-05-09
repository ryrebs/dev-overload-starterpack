# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
from scrapy.exceptions import DropItem


class WebscraperappPipeline(object):

    def process_item(self, item, spider):
        if spider.name == '<spider-here>':
            if re.search():
                # <logic here>
                raise DropItem(item)

        return item
