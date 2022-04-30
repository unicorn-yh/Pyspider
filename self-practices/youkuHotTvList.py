#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2021-11-23 21:51:09
# Project: youkuHotTvList

from pyspider.libs.base_handler import *
from bs4 import BeautifulSoup

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://tv.youku.com/', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)
            
        #使用pyquery定位过滤
        Tag=response.doc('div[class="yk-rank yk-rank-long"]')
        subTags=Tag('div[class="item"]').items()
        for tag in subTags:
            fileName=tag('a').text()
            href=tag('a').attr.href
            playNum=tag('span[class="extend"]').text()
            print('%s, %s, %s'%(playNum,fileName,href))

        #使用bs4过滤定位
        soup=BeautifulSoup(response.text,'lxml')
        Tag=soup.find('div',attrs={'class':'yk-rank yk-rank-long'})
        subTags=Tag.find_all('div',attrs={'class':'item'})
        for tag in subTags:
            fileName=tag.find('a').get_text()
            href=tag.find('a').get('href')
            playNum=tag.find('span',attrs={'class':'extend'}).get_text()
            print('%s, %s, %s'%(playNum,fileName,href))

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
