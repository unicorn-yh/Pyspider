#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2021-11-24 17:32:58
# Project: doubanmovie

from pyspider.libs.base_handler import * 
import os

class Handler(BaseHandler): base_dir = "D:/yh/YH2021/Python/doubanmovie"

crawl_config = {
}

@every(minutes=24 * 60)
def on_start(self):
    self.crawl('https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%BB%8F%E5%85% B8&sort=rank&page_limit=30&page_start=0',validate_cert=False, callback=self.index_page)

@config(age=10 * 24 * 60 * 60) 
def index_page(self, response):
    for m in response.json["subjects"]:
        self.crawl(m["url"],validate_cert=False, callback=self.mv_page)

@config(age=10 * 24 * 60 * 60) 
def mv_page(self, response):  #电影名
    mv_name = response.doc("h1 > span").text().encode("gbk") #电影描述
    mv_desc = response.doc("#info").text().encode("gbk") #电影图片地址
    mv_img_url = response.doc("#mainpic img").attr.src;

    mv_dir = self.base_dir+"\\"+mv_name   #创建该电影的文件夹
    if not os.path.exists(mv_dir): 
        os.makedirs(mv_dir)     #创建文本文件保存电影描述
        mv_file = open(mv_dir+"\\"+mv_name+".txt","w")
        mv_file.write(mv_desc) 
        mv_file.flush() 
        mv_file.close()
        #下载封面图片
        ###封面图片存储路径
        mv_img_path = mv_dir+"\\"+mv_img_url.split("/")[-1] ###爬取封面图片
        self.crawl(mv_img_url,validate_cert=False,callback=self.mv_img_down,save={"mv_img_path":mv_img_path}) #爬取剧照页面
        mv_photos_url = response.doc(".related-pic .pl > a:nth-child(4)").attr.href 
        self.crawl(mv_photos_url,validate_cert=False,callback=self.mv_photos_page,save={"mv_dir":mv_dir})

@config(age=10 * 24 * 60 * 60)
def mv_photos_page(self, response):
    photoAncrArr = response.doc(".article li a").items() 
    for photoAncr in photoAncrArr:
        self.crawl(photoAncr.attr.href,validate_cert=False, callback=self.mv_photo_page,save=response.save)

@config(age=10 * 24 * 60 * 60)
def mv_photo_page(self, response): #存储位置
    photos_path=response.save["mv_dir"]+"\\photo" 
    if not os.path.exists(photos_path): 
        os.makedirs(photos_path) #图片url
    img_url = response.doc(".mainphoto > img").attr.src 
    self.crawl(img_url,validate_cert=False,callback=self.mv_img_down,save={"mv_img_path":photos_path+"\\"+img_url.split("/")[-1]})

@config(age=10 * 24 * 60 * 60) 
def mv_img_down(self, response):
    img_data = response.content
    img_file = open(response.save["mv_img_path"],"wb") 
    img_file.write(img_data)
    img_file.flush() 
    img_file.close()
