# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsGatherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PaperSeebugItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    save_path = scrapy.Field()
    origin = scrapy.Field()
