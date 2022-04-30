from pyspider.libs.base_handler import *
from bs4 import BeautifulSoup
import urllib
from urllib import parse
import csv
import requests

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    'Host' : 'search.51job.com',
    'Upgrade-Insecure-Requests' : '1'
}

key='数据挖掘'   #只爬取数据挖掘的数据，用户可以更换关键字爬取其他行业数据
key=parse.quote(parse.quote(key))   #编码调整，如将“数据挖掘”编码成%25E6%2595%25B0%25E6%258D%25AE%25E6%258C%2596%25E6%258E%2598
city='北京'
city=parse.quote(parse.quote(city))


class Handler(BaseHandler):
    crawl_config = {
        "connect_timeout": 100,
        "timeout": 600,
        "retries": 15,
    }
    
    def __init__(self):
        self.basedir = "D:/yh/YH2021/Python/51zhaopin"
        self.head=["职位","公司","地点","薪资","公司类型","规模","行业","经验","学历","招聘人数","福利","职位要求","链接"]  #表头
        self.urls=[]
        self.datas=[]
        self.datas.append(self.head)
        self.tempdata=[]
        self.zhiwei,self.gongsi,self.didian,self.xinzi,self.gongsileixing,self.guimo,self.hangye,self.jingyan,self.xueli,self.renshu,self.fuli,self.zhiweiyaoqiu,self.lianjie="","","","","","","","","","","","",""
        for page in range(1,24):
            #url ='http://search.51job.com/list/'+city+',000000,0000,00,9,99,'+key+',2,'+str(page)+'.html'
            url ='http://search.51job.com/list/010000,000000,0000,00,9,99,'+key+',2,'+str(page)+'.html'
            self.urls.append(url)
    
    @every(minutes=24 * 60)
    def on_start(self):
        for url in self.urls:
            self.crawl(url,callback=self.index_page,validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):   #下一页
        #pagenum=(response.doc('div[class="rt rt_page"]').text().split('/'))[1].strip()
        #pagenum=int(pagenum)
        try:
            Tag=response.doc('div[class="j_joblist"]')
        except Exception as e:
            pass
        for tag in Tag('div[class="e"]').items():
            try:
                self.zhiwei=tag.find("jname at").text().strip()
                self.gongsi=tag.find("cname at").text().strip()
                self.didian=(tag.find("d at").text().split('|'))[0].strip()
                self.xinzi=tag.find("sal").text().strip()
                self.gongsileixing=(tag.find("dc at").text().split('|'))[0].strip()
                self.guimo=(tag.find("dc at").text().split('|'))[1].strip()
                self.hangye=tag.find("int at").text().strip()
                self.jingyan=(tag.find("d at").text().split('|'))[1].strip()
                self.xueli=(tag.find("d at").text().split('|'))[2].strip()
                self.renshu=(tag.find("d at").text().split('|'))[3].strip()
                self.fuli=tag.find("tags").attr("title")
                #daterelease
                #zhiweiyaoqiu
                self.lianjie=tag.find("el").attr("href")
            except Exception as e:
                pass
            self.crawl(self.lianjie,callback=self.detail_page,validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        self.tempdata=[self.zhiwei,self.gongsi,self.didian,self.xinzi,self.gongsileixing,self.guimo,self.hangye,self.jingyan,self.xueli,self.renshu,self.fuli,self.zhiweiyaoqiu,self.lianjie]
        print(self.tempdata)
        self.datas.append(self.tempdata)
        tempdict={
                "职位":self.zhiwei,
                "公司":self.gongsi,
                "地点":self.didian,
                "薪资":self.xinzi,
                "公司类型":self.gongsileixing,
                "规模":self.guimo,
                "行业":self.hangye,
                "经验":self.jingyan,
                "学历":self.xueli,
                "招聘人数":self.renshu,
                "福利":self.fuli,
                "职位要求":self.zhiweiyaoqiu,
                "链接":self.lianjie
            }
        #return tempdict

        
        with open('"C:\\Users\\User\\Desktop\\51data.csv','a',encoding='utf-8',newline='') as csvfile:
            writer=csv.DictWriter(csvfile,fieldnames=self.head)
            writer.writeheader()
            writer.writerow(tempdict)
        return self.datas
