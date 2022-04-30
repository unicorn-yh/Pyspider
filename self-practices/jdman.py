#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-01-23 10:25:59
# Project: JD
 
from pyspider.libs.base_handler import *
import os
 
class Handler(BaseHandler):
    crawl_config = {
    }
    def __init__(self):
        self.base_dir ="D:/yh/YH2021/Python/jdman"
 
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://search.jd.com/Search?keyword=%E7%94%B7%E8%A3%85&enc=utf-8&wq=%E7%94%B7%E8%A3%85&pvid=97c29de04971462aac5bc8d7a6f3b829',callback=self.index_page,validate_cert=False)
 
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):        
        for ide in response.doc(".sl-v-logos > ul li a").items():
            mk_name=ide.text().encode("gbk")
            mk_text=ide.attr("href")+'\n' 
            mk_dir=self.base_dir+"\\"+mk_name
            img_name=mk_dir+"\\"+"img"
            if not os.path.exists(mk_dir):
                os.mkdir(mk_dir)
            if not os.path.exists(img_name):
                os.mkdir(img_name) 
        text_name=open(mk_dir+"\\"+mk_name+".txt","w")
        text_name.write(mk_text)
        text_name.flush()
        text_name.close()
               
        for img in response.doc(".sl-v-logos > ul li a img").items():
            
            print img.attr("src")+'\n'
            img_url=img.attr("src")
            self.crawl(img_url,callback=self.img1_page,validate_cert=False,save={"img_url":img_url})        
        
 
        
    @config(age=10 * 24 * 60 * 60)
    def img1_page(self, response):
        img1_page=response.save['img_url']
        print(img1_page)
        img_data=response.content         
        img_file=open(img1_page)
        img_file.write(img_data)
        img_file.flush()
        img_file.close()
                
        
        
        
        
        
        