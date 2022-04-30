from pyspider.libs.base_handler import *
from bs4 import BeautifulSoup
import urllib
from urllib import parse
import csv
import requests
import re

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    'Host' : 'search.51job.com',
    'Upgrade-Insecure-Requests' : '1'
}
headers={
    'Host':'search.51job.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Content-Type': 'application/json',
    'accept': 'application/json',
    "Accept-Encoding": "*",
    "Connection": "keep-alive"

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
        head=["职位","公司","地点","薪资","公司类型","规模","行业","经验","学历","招聘人数","福利","职位要求","链接"]  #表头
        self.urls=[]
        for page in range(1,24):
            #url ='http://search.51job.com/list/'+city+',000000,0000,00,9,99,'+key+',2,'+str(page)+'.html'
            url ='http://search.51job.com/list/010000,000000,0000,00,9,99,'+key+',2,'+str(page)+'.html'
            self.urls.append(url)
    
    @every(minutes=24 * 60)
    def on_start(self):
        for url in self.urls:
            self.crawl(url,callback=self.index_page,validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):    #下一页
        #tmpp = response.doc('body > div:nth-child(4) > div.j_result > div > div.leftbox > div:nth-child(4) > div.j_joblist')
        r= requests.post(response.url,environ.get('customer_api_url'),headers=headers,json=lead,timeout=10)
        #r= requests.get(response.url,headers=headers,timeout=10)
        s=requests.session()
        s.keep_alive = False
        r.encoding = 'gbk'
        reg = re.compile(r'class="t1 ">.*? <a target="_blank" title=".*?" href="(.*?)".*? <span class="t2">', re.S)
        links = re.findall(reg, r.text)     #拥有一对链接的数组
        for link in links:  
            self.crawl(link,callback=self.detail_page,validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        try:
            zhiwei = response.doc('h1').text()
            gongsi = response.doc('body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > p.cname > a.catn').text()
            tmp = response.doc('body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > p.msg.ltype').text().strip()
            tmp = tmp.replace('&nbsp;','').replace('<span>','').replace('"','').replace('</span>','')
            tmp = tmp.split('|')
            didian = tmp[0].strip()
            xinzi = response.doc('body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > strong').text()
            gongsileixing = response.doc('body > div.tCompanyPage > div.tCompany_center.clearfix > div.tCompany_sidebar > div:nth-child(1) > div.com_tag > p:nth-child(1)').text()
            guimo = response.doc('body > div.tCompanyPage > div.tCompany_center.clearfix > div.tCompany_sidebar > div:nth-child(1) > div.com_tag > p:nth-child(2)').text()
            hangye = response.doc('body > div.tCompanyPage > div.tCompany_center.clearfix > div.tCompany_sidebar > div:nth-child(1) > div.com_tag > p:nth-child(3)').text()
            jingyan = tmp[1].strip()
            try: xueli = tmp[2].strip()
            except: xueli = '无'
            renshu = tmp[3].strip()

            fuli = response.doc('body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > div > div').text()
            lianjie = response.url  #response.meta['url']
            zhiweiyaoqiu = re.findall(r'<div class="bmsg job_msg inbox">(.*?)<div class="mt10">', response.text, re.I|re.S|re.M)[0]\
            .replace('\r', '').replace('\n', '').replace('\t', '').replace('\xa0', '').replace('<br>', '')\
            .replace('<br/>', '').replace('<P>', '').replace('</P>', '').replace('?', ' ').replace('<p>', '').replace('</p>', '')\
            .replace('<div>', '').replace('</div>', '').replace('<BR>', '').replace('</BR>', '').replace('&nbsp;','')
            zhiweiyaoqiu = zhiweiyaoqiu.split('公司介绍')[0]
        except Exception as e:
            pass
        tempdict={
                "职位":zhiwei,
                "公司":gongsi,
                "地点":didian,
                "薪资":xinzi,
                "公司类型":gongsileixing,
                "规模":guimo,
                "行业":hangye,
                "经验":jingyan,
                "学历":xueli,
                "招聘人数":renshu,
                "福利":fuli,
                "职位要求":zhiweiyaoqiu,
                "链接":lianjie
        }
        return tempdict
