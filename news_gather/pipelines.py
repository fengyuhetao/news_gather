# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from twisted.enterprise import adbapi


class NewsGatherPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    # 采用同步机制写入数据库
    def __init__(self):
        self.conn = pymysql.connect('localhost', 'root', '', 'crawl', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # 执行具体的插入
        sql = """
                  insert into telescope(title, content, url, save_path, origin, create_time) values(%s, %s, %s, %s, %s, %s)
                """
        self.cursor.execute(sql, (item['title'], item['content'], item['url'], item['save_path'], item['origin'], item['create_time']))
        self.conn.commit()


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host = settings["MYSQL_HOST"],
            user = settings["MYSQL_USER"],
            password = settings["MYSQL_PASSWORD"],
            db = settings["MYSQL_DB"],
            charset = 'utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode = True
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted 将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    @staticmethod
    def handle_error(failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        sql = """
          insert into telescope(title, content, url, save_path, origin, create_time) values(%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (item['title'], item['content'], item['url'], item['save_path'], item['origin'], item['create_time']))
