#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2021-11-24 14:29:06
# Project: qunarSql

from pyspider.libs.base_handler import *
import pymysql

class Handler(BaseHandler):
    crawl_config = {
    }

    # 连接数据库
    def __init__(self):   #连接数据库等初始化
        self.db = pymysql.connect(host='localhost',user='root',password='981220',database='qunar',charset='utf8')
 
    def save_in_mysql(self, url, title, date, day, who, text, image):
        try:
            cursor = self.db.cursor()
            sql = 'INSERT INTO qunar(url, title, date, day, who, text, image) \
            VALUES (%s, %s , %s, %s, %s, %s, %s)'   # 插入数据库的SQL语句
            print(sql)
            cursor.execute(sql, (url, title, date, day, who, text, image))
            print(cursor.lastrowid)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://travel.qunar.com/travelbook/list.htm', callback=self.index_page, validate_cert=False)
 
    @config(age=100 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('li > .tit > a').items():
            self.crawl(each.attr.href, callback=self.detail_page, validate_cert=False, fetch_type='js')
        next = response.doc('.next').attr.href
        self.crawl(next, callback=self.index_page)
 
    @config(priority=2)
    def detail_page(self, response):  #调用save_in_mysql函数:
        url = response.url
        title = response.doc('title').text()
        date = response.doc('.when .data').text()
        day = response.doc('.howlong .data').text()
        who = response.doc('.who .data').text()
        text = response.doc('#b_panel_schedule').text()[0:100].replace('\"', '\'', 10)
        image = response.doc('.cover_img').attr.src       #插入数据库
        self.save_in_mysql(url, title, date, day, who, text, image)  #表头 
        return {
            "url": response.url,
            "title": response.doc('#booktitle').text(),
            "date": response.doc('.when .data').text(),
            "day": response.doc('.howlong .data').text(),
            "who": response.doc('.who .data').text(),
            "text": response.doc('#b_panel_schedule').text(),
            "image": response.doc('.cover_img').text(),
        }