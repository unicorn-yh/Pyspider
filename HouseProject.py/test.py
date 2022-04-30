#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2021-12-13 00:34:02
# Project: house

from pyspider.libs.base_handler import *
import xlwt
import xlrd
from xlutils.copy import copy
import unicodedata
from lxml import html

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    'Host' : 'm.lianjia.com',
    'Upgrade-Insecure-Requests' : '1'
}

def set_excel():
    wb = xlwt.Workbook()
        # 2.创建 worksheet
    ws = wb.add_sheet('Beijing')
        # 3.写入第一行内容  ws.write(a, b, c)  a：行，b：列，c：内容
    for i in range (20):
        ws.col(i).width = 3500
    style = xlwt.easyxf('pattern: pattern solid;''font: colour orange, bold True, height 280;')
    default_style = xlwt.easyxf('font: colour black, bold True, height 225;')
    ws.write(0, 0, '链家二手房记录', style=style)
    ws.write(1, 0, '标题', style=default_style)
    ws.write(1, 1, '链家编号', style=default_style)
    ws.write(1, 2, '挂牌时间', style=default_style)
    ws.write(1, 3, '户型', style=default_style)
    ws.write(1, 4, '面积', style=default_style)
    ws.write(1, 5, '楼层', style=default_style)
    ws.write(1, 6, '地址', style=default_style)
    ws.write(1, 7, '建造时间', style=default_style)
    ws.write(1, 8, '房屋年限', style=default_style)
    ws.write(1, 9, '房屋权属', style=default_style)
    ws.write(1, 10, '房屋用途', style=default_style)
    ws.write(1, 11, '上次交易时间', style=default_style)
    ws.write(1, 12, '房屋朝向', style=default_style)
    ws.write(1, 13, '小区名称', style=default_style)
    ws.write(1, 14, '小区均价', style=default_style)
    ws.write(1, 15, '交易属性', style=default_style)
    ws.write(1, 16, '整户价格', style=default_style)
    ws.write(1, 17, '平米单价', style=default_style)
    ws.write(1, 18, '中介咨询电话', style=default_style)
    ws.write(1, 19, '详情链接', style=default_style)
    wb.save('D:\\myExcel.xls')

def save_to_excel(dic):
    workbook = xlrd.open_workbook('D:\\myExcel.xls', formatting_info=True)
    sheet = workbook.sheet_by_index(0)
    rowNum = sheet.nrows
    newbook = copy(workbook)
    newsheet = newbook.get_sheet(0)	
    i=0
    for value in dic.values():
        newsheet.write(rowNum, i, value)
        i=i+1
    newbook.save('D:\\myExcel.xls')

class Handler(BaseHandler):
    crawl_config = {
    }
        
    @every(minutes=24 * 60)
    def on_start(self):
        set_excel()
        for index in range(1, 101):
            url = 'https://bj.lianjia.com/ershoufang/'+'pg'+str(index)+'co32/'
            self.crawl(url, callback=self.index_page,validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('#content > div.leftContent > ul > li > div.info.clear > div.title > a').items():
            self.crawl(each.attr.href, callback=self.detail_page,validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        r1=requests.get(response.url,headers,timeout=10)
        s=requests.session()
        s.keep_alive = False
        r1.encoding = 'gb2312'
        t1=html.fromstring(r1.text)
        #print(link)
        #job=t1.xpath('//div[@class="tHeader tHjob"]//h1/text()')[0].strip()
        house={}
        house['biaoti'] = response.doc('title').text()
        house['bianhao'] = response.doc('body > div.overview > div.content > div.aroundInfo > div.houseRecord > span.info ').text()[0:-2]
        house['guapai'] = response.doc('#introduction > div > div > div.transaction > div.content > ul > li:nth-child(1) > span:nth-child(2)').text()
        house['huxing'] = response.doc('body > div.overview > div.content > div.houseInfo > div.room > div.mainInfo ').text()
        house['square'] = response.doc('body > div.overview > div.content > div.houseInfo > div.area > div.mainInfo').text()
        house['louceng'] = response.doc('body > div.overview > div.content > div.houseInfo > div.room > div.subInfo ').text()
        house['address'] = unicodedata.normalize("NFKD",response.doc('body > div.overview > div.content > div.aroundInfo > div.areaName > span.info ').text())
        house['jianzao'] = response.doc('body > div.overview > div.content > div.houseInfo > div.area > div.subInfo.noHidden ').text()[0:6]
        house['nianxian'] = response.doc('#introduction > div > div > div.transaction > div.content > ul > li:nth-child(5) > span:nth-child(2)').text()
        house['quanshu'] = response.doc('#introduction > div > div > div.transaction > div.content > ul > li:nth-child(2) > span:nth-child(2) ').text()
        house['yongtu'] = response.doc('#introduction > div > div > div.transaction > div.content > ul > li:nth-child(4) > span:nth-child(2) ').text()
        house['lasttime'] = response.doc('#introduction > div > div > div.transaction > div.content > ul > li:nth-child(3) > span:nth-child(2) ').text()
        house['chaoxiang'] = response.doc('body > div.overview > div.content > div.houseInfo > div.type > div.mainInfo ').text()
        house['xiaoqu'] = response.doc('body > div.overview > div.content > div.aroundInfo > div.communityName > a.info ').text()
        house['junjia'] = response.doc('body > div.overview > div.content > div.price > div.text > div.unitPrice > span').text()
        house['jiaoyi'] = response.doc('div.transaction > div.content > ul > li > span:nth-child(2)').text()
        house['price'] = response.doc(' body > div.overview > div.content > div.price > span.total ').text()+'万'
        house['danjia'] = response.doc(' body > div.overview > div.content > div.price > div.text > div.unitPrice > span ').text()
        house['zhongjie'] = response.doc('#zuanzhan > div.component-agent-es-pc-2 > div > div.ke-agent-sj-sdk-f-0.ke-agent-sj-bottom > div.ke-agent-sj-phone ').text()
        house['lianjie']=response.url
        save_to_excel(house)
        return house
        
        
        
        