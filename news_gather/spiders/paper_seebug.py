# -*- coding: utf-8 -*-
from urllib import parse
from scrapy.http import Request
import scrapy


class PaperSeebugSpider(scrapy.Spider):
    name = 'paper_seebug'
    allowed_domains = ['https://paper.seebug.org']
    start_urls = ['http://paper.seebug.org//']

    base_url = "http://paper.seebug.org/"
    base_category_url = "https://paper.seebug.org/category/"
    # categorys = ['vul-analysis', 'tools', 'information', 'experience', 'web-security', 'bin-security',
    #              'mobile-security', 'prime', 'ctf', 'IoT', 'blockchain']
    categorys = ['vul-analysis']



    # headers = {
    #     "HOST": "https://paper.seebug.org",
    #     "Referer": "https://paper.seebug.org",
    #     'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    # }

    def start_requests(self):
        for category in self.categorys:
            url = self.base_category_url + category + '/'
            yield Request(url, dont_filter=True, callback=self.parse)

    def deal_page(self, response):
        post_nodes = response.css("#wrapper > main > div > article > header > h5 > a")
        for post_node in post_nodes:
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(self.base_url, post_url), callback=self.parse)

        # 提取下一页并交给scrapy进行下载
        next_url = response.css("#wrapper > main > div > nav > a::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.deal_page)
        pass

    def parse(self, response):

        pass
