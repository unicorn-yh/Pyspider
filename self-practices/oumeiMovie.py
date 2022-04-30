#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2021-11-24 00:57:45
# Project: oumeiMovie

from pyspider.libs.base_handler import *
from bs4 import BeautifulSoup
import re
import codecs

class Handler(BaseHandler):
    crawl_config = {
    }
    def __init__(self):    #构造函数
        self.urls=[]       #统计所有需要爬的页面
        for page in range(1,267+1):
            url='https://www.ygdy8.net/html/gndy/oumei/list_7_'+str(page)+'.html'
            self.urls.append(url)

    @every(minutes=24 * 60)
    def on_start(self):
        for url in self.urls:
            self.crawl(url, callback=self.index_page, validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):  #获取电影名称和下载页面，通过电影下载页面链接回调detail_page函数获取最终数据
        soup=BeautifulSoup(response.text,'html.parser')   #有 a class 用 beautifulsoup 比较方便
        try:
            Tags=soup.find_all('table',attrs={'width':'100%','border':'0','cellspacing':'0','cellpadding':'0','class':'tbspan','style':'margin-top:6px'})
        except Exception as e:
            pass
        for tag in Tags:
            try:
                movieName=tag.find_all('a')[-1].get_text()
                movieHref=tag.find_all('a')[-1].get('href')
                url='http://www/ygdy8/com'+movieHref
            except Exception as e:
                pass
            self.crawl(url, callback=self.detail_page,save={'movieName':movieName},validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        movieName=response.save.get('movieName')
        html=re.sub('<br />{1,5}','',response.text)
        try:
            dataStr=re.search(u'◎.*<', html).group()
        except Exception as e:
            pass
        soup=BeautifulSoup(response.text,'html.parser')
        try:
            hrefTag=soup.find('td',attrs={'style':'WORD-WRAP:break-word','bgcolor':'#fdfddf'})
        except Exception as e:
            pass
        dataList=dataStr.split(u'◎')    #在中文字符前加上u，字符编码为unicode
        dataDic = {u'译名':'',u'片名':'',u'年代':'',u'产地':'',u'类别':'',u'语言':'',u'字幕':'', u'IMDb评分':'',u'豆瓣评分':'',u'文件格式':'',u'downUrl':href,u'视频尺寸':'',u'文件大小':'',u'片长':'',u'导演':'',u'主演':'',u'简介':'',u'movieName':movieName}
        for key in dataDic.keys():
            for st in dataList:
                if re.search(key,st):
                    dataDic[key]=re.sub(key,'',st)
                    break
        return dataDic
