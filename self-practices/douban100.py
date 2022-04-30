#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-01-21 11:20:39
# Project: DBDY
 
from pyspider.libs.base_handler import *
import os
 
class Handler(BaseHandler):
    crawl_config = {
    }
    
    def __init__(self):
        self.basedir = "D:/yh/YH2021/Python/douban100"
 
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%BB%8F%E5%85%B8&sort=recommend&page_limit=30&page_start=0', callback=self.index_page ,validate_cert=False)
 
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for obj in response.json["subjects"]:
            save = {'id':obj['id'],'title':obj['title'],'mvdir':self.basedir+"/"+obj['title']}
            if not os.path.exists(save['mvdir']):
                os.mkdir(save['mvdir'])     #创建文件夹
            self.crawl(obj["url"], callback=self.mv_page ,validate_cert=False,save=save)
            self.crawl("https://movie.douban.com/subject/"+obj['id']+"/all_photos", callback=self.photos_page ,validate_cert=False,save=save)
    @config(age=10 * 24 * 60 * 60)
    def mv_page(self, response):
        desc = response.doc("#info").text().encode("gbk")
        f = open(response.save['mvdir']+"/"+response.save['title']+".txt","w")#在文件夹下创建一个子文件夹
        f.write(desc)
        f.flush()
        f.close()
        #phototsurl = response.doc(".related-pic .pl > a:nth-child(4)").attr.href  #得到图片的地址--a:nth-child(4)--第4个子元素
        #self.crawl(phototsurl, callback=self.photos_page ,validate_cert=False,save=mvdir)
    
    @config(age=10 * 24 * 60 * 60)
    def photos_page(self, response):
        for obj in response.doc('.article li > a').items(): #选取图片的源地址(单个图片的地址)
            self.crawl(obj.attr.href, callback=self.photo_page ,validate_cert=False,save=response.save)
    
    @config(age=10 * 24 * 60 * 60)
    def photo_page(self, response):
        imgurl = response.doc('.mainphoto > img').attr.src  #得到大图片的地址
        mvdir = response.save['mvdir']
        imgname = imgurl.split("/")[-1]  #--选取最后一个最为图片名
        imgpath = mvdir+"/"+imgname  #图片的地址
        self.crawl(imgurl, callback=self.downimg_page ,validate_cert=False,save=imgpath)
    
    @config(age=10 * 24 * 60 * 60)
    def downimg_page(self, response):
        data = response.content
        f = open(response.save,'wb') #以二进制写出数据wb
        f.write(data)
        f.flush()
        f.close()