# -*- coding: utf-8 -*-
__author__ = "ht"

from scrapy.cmdline import execute
import sys
import os
print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    execute(["scrapy", "crawl", "paper_seebug"])