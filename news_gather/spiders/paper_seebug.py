# -*- coding: utf-8 -*-
import scrapy


class PaperSeebugSpider(scrapy.Spider):
    name = 'paper_seebug'
    allowed_domains = ['https://paper.seebug.org/']
    start_urls = ['http://https://paper.seebug.org//']

    def parse(self, response):

        pass
