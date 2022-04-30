#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2021-11-24 13:35:33
# Project: musicTop

from pyspider.libs.base_handler import *
import random

headers={
    "Accept":"text/html,application/xhtml+xml,application/xml;a=0.9,image/webp,iamge/apng,*/*;q=0.8",
    "Accept-Encoding":"gzip,deflate",
    "Accept-Language":"en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "User-Agent":"Mozilla/5.0(Windows NT 10.0;Win64;x64)AppleWebKit/537.36(KHTML,like Gecko)Chrome/63.0.3239.84 Safari/537.36"
}
proxyList=["192.168.1.99:1080","101.68.73.54:53281",""]

class Handler(BaseHandler):
    crawl_config = {
       # "proxy":proxy,
       # "headers":headers
    }

    def __init__(self):
        url='http://vchart.yinyuetai.com/vchart/trends?area=ML&page='
        pages=['1','2','3']
        self.urls=[]
        for page in pages:
            self.urls.append(url+page)

    @every(minutes=24 * 60)
    def on_start(self):
        for url in self.urls:
            self.crawl(url, callback=self.index_page,proxy=random.choice(proxyList),headers=headers,validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        #for each in response.doc('a[href^="http"]').items():
            #self.crawl(each.attr.href, callback=self.detail_page,validate_cert=False)
        Tags=response.doc('li[class="vitem J_li_toggle_date"]').items()
        for subTag in Tags:
            top_num=subTag('div[class="top_num"]').text()
            mvname=subTag('a[class="mvname"]').text()
            singer=subTag('a[class="special"]').text()
            desc_score=subTag('h2[class="special"]').text()
            print('%s %s %s %s'%(top_num,mvname,singer,desc_score))

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
