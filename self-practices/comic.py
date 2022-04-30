#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-06-03 21:52:13
# Project: test

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.mmonly.cc/ktmh/hzw/list_34_1.html', callback=self.index_page,validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        #下一页
        for each in response.doc('.title a').items():
            self.crawl(each.attr.href, callback=self.detail,validate_cert=False)
        #抓取内容页
        url = response.doc('#pageNum > a:nth-last-child(2)').attr.href
        if url:
            self.crawl(url, callback=self.index_page,validate_cert=False) 

    @config(age=10 * 24 * 60 * 60)
    def detail(self, response):
        #详情页面
        #print response.doc('#contbody > div > div > a > img').attr('src')
        self.crawl(response.url+'?time=1', callback=self.detail_page,validate_cert=False) 
        #其他页面
        next_url = response.doc('#nl a').attr.href
        #print next_url
        #for each in response.doc('.pages a:last').items():
        if next_url != None and not next_url.endswith('##'):
            self.crawl(next_url, callback=self.detail,validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "img": response.doc('p img').attr('src')
        }