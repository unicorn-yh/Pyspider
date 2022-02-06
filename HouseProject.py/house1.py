#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2021-12-13 00:34:02
# Project: house

from pyspider.libs.base_handler import *
import xlwt
import xlrd
from xpinyin import Pinyin
from xlutils.copy import copy
import unicodedata
import re

city='北京'   #根据用户需求，用户可自行更改想要查询的城市

def get_city():    #获取城市每个词汉语拼音的首个英文字母
    s = Pinyin().get_pinyin(city).split('-')
    ls=""
    for item in s:
        ls+=item[0]
    return ls

def set_excel():
    wb = xlwt.Workbook()              # 创建 worksheet
    ws = wb.add_sheet(city)           # 创建工作表
    for i in range (20):
        ws.col(i).width = 3500        # 设置每列的宽度，方便用户浏览
    style = xlwt.easyxf('pattern: pattern solid;''font: colour orange, bold True, height 280;')  #设置字样和格式
    default_style = xlwt.easyxf('font: colour black, bold True, height 225;')
    ws.write(0, 0, '链家二手房记录：'+city, style=style)   # 写入第一行标题  ws.write(a, b, c)  a：行，b：列，c：内容
    ws.write(1, 0, '标题', style=default_style)
    ws.write(1, 1, '链家编号', style=default_style)
    ws.write(1, 2, '挂牌时间', style=default_style)
    ws.write(1, 3, '户型', style=default_style)
    ws.write(1, 4, '面积(平米)', style=default_style)
    ws.write(1, 5, '楼层', style=default_style)
    ws.write(1, 6, '地址', style=default_style)
    ws.write(1, 7, '建造时间(年)', style=default_style)
    ws.write(1, 8, '房屋年限', style=default_style)
    ws.write(1, 9, '房屋权属', style=default_style)
    ws.write(1, 10, '房屋用途', style=default_style)
    ws.write(1, 11, '上次交易时间', style=default_style)
    ws.write(1, 12, '房屋朝向', style=default_style)
    ws.write(1, 13, '小区名称', style=default_style)
    ws.write(1, 14, '小区均价(元/平米)', style=default_style)
    ws.write(1, 15, '交易属性', style=default_style)
    ws.write(1, 16, '整户价格(万)', style=default_style)
    ws.write(1, 17, '平米单价(元/平米)', style=default_style)
    ws.write(1, 18, '中介咨询电话', style=default_style)
    ws.write(1, 19, '详情链接', style=default_style)
    wb.save('D:/'+city+'二手房.xls')

def save_to_excel(dic):
    workbook = xlrd.open_workbook('D:/'+city+'二手房.xls', formatting_info=True)
    sheet = workbook.sheet_by_index(0)
    rowNum = sheet.nrows
    newbook = copy(workbook)
    newsheet = newbook.get_sheet(0)	
    i=0
    for value in dic.values():
        newsheet.write(rowNum, i, value)
        i=i+1
    newbook.save('D:/'+city+'二手房.xls')


class Handler(BaseHandler):
    crawl_config = {
        'headers' : {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
        },
        'cookies' : {
        "_T_WM":"791e0d5962c38c757bead1a106a4dcc5",
        " ALF":"1489404939",
        " SCF":"AmNkSminRmi2L6WiP0tbn2H_p-TOZQIRRTLwEL5OhwHOohm56wHRk_9Jy1w7iXftduUAJihNuU3B-8cYnWBT3Lk.",
        " SUB":"_2A251modoDeRxGeNG7VEV9ibIyT6IHXVXZCkgrDV6PUJbktBeLXXZkW2HyTgXsruSYnviSU7hXUjfdGTOig..",
        " SUBP":"0033WrSXqPxfM725Ws9jqgMF55529P9D9W5wqBjzJ2m1XohsTfpMwPVx5JpX5o2p5NHD95Qf1hq0ShqRShzEWs4Dqcjci--fi-i8iK.7i--fi-2Xi-2Ni--fi-2Xi-2Ni--fi-2Xi-2Ni--fi-2Xi-2Ni--fi-zRiKnf",
        " SUHB":"0tKqtAdy5rivMy",
        " SSOLoginState":"1486812984"
        }
    }
        
    def __init__(self):
        self.urls=[]
        totalpage=100
        for index in range(1,totalpage+1):
            url = 'https://'+get_city()+'.lianjia.com/ershoufang/pg'+str(index)+'/'
            self.urls.append(url)   

    @every(minutes=24 * 60)
    def on_start(self):
        set_excel()
        for url in self.urls:
            self.crawl(url, callback=self.index_page, validate_cert=False, auto_recrawl=True, connect_timeout=17, timeout=150, force_update=True, last_modified=True, itag='v1', retries=5, priority=0, method="GET") 

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('#content > div.leftContent > ul > li > div.info.clear > div.title > a').items():
            self.crawl(each.attr.href, callback=self.detail_page, validate_cert=False, auto_recrawl=True, connect_timeout=17, timeout=150, force_update=True, last_modified=True, itag='v1', retries=5, priority=0, method="GET")

    @config(priority=2)
    def detail_page(self, response):
        house={}
        house['biaoti'] = response.doc('title').text()
        house['bianhao'] = format(float(response.doc('body > div.overview > div.content > div.aroundInfo > div.houseRecord > span.info ').text()[0:-2]),'.0f')
        house['guapai'] = response.doc('#introduction > div > div > div.transaction > div.content > ul > li:nth-child(1) > span:nth-child(2)').text()
        house['huxing'] = response.doc('body > div.overview > div.content > div.houseInfo > div.room > div.mainInfo ').text()
        house['square'] = format(float(re.sub("[^0-9]","",response.doc('body > div.overview > div.content > div.houseInfo > div.area > div.mainInfo').text())),'.2f')
        house['louceng'] = response.doc('body > div.overview > div.content > div.houseInfo > div.room > div.subInfo ').text()
        house['address'] = unicodedata.normalize("NFKD",response.doc('body > div.overview > div.content > div.aroundInfo > div.areaName > span.info ').text())
        house['jianzao'] = re.sub("[^0-9]","",response.doc('body > div.overview > div.content > div.houseInfo > div.area > div.subInfo.noHidden ').text()[0:6])
        if house['jianzao']=="":
            house['jianzao']="未知"
        house['nianxian'] = response.doc('#introduction > div > div > div.transaction > div.content > ul > li:nth-child(5) > span:nth-child(2)').text()
        house['quanshu'] = response.doc('#introduction > div > div > div.transaction > div.content > ul > li:nth-child(2) > span:nth-child(2) ').text()
        house['yongtu'] = response.doc('#introduction > div > div > div.transaction > div.content > ul > li:nth-child(4) > span:nth-child(2) ').text()
        house['lasttime'] = response.doc('#introduction > div > div > div.transaction > div.content > ul > li:nth-child(3) > span:nth-child(2) ').text()
        house['chaoxiang'] = response.doc('body > div.overview > div.content > div.houseInfo > div.type > div.mainInfo ').text()
        house['xiaoqu'] = response.doc('body > div.overview > div.content > div.aroundInfo > div.communityName > a.info ').text()
        house['junjia'] = format(float(re.sub("[^0-9]","",response.doc('body > div.overview > div.content > div.price > div.text > div.unitPrice > span').text())),'.2f')
        #resblockCardContainer > div > div > div.xiaoqu_content.clear > div > div:nth-child(1) > span
        house['jiaoyi'] = response.doc('  div.transaction > div.content > ul > li > span:nth-child(2) ').text()
        house['price'] = format(float(re.sub("[^0-9]","",response.doc(' body > div.overview > div.content > div.price > span.total ').text())),'.2f')
        house['danjia'] = format(float(re.sub("[^0-9]","",response.doc(' body > div.overview > div.content > div.price > div.text > div.unitPrice > span ').text())),'.2f')
        house['zhongjie'] = response.doc('#zuanzhan > div.component-agent-es-pc-2 > div > div.ke-agent-sj-sdk-f-0.ke-agent-sj-bottom > div.ke-agent-sj-phone ').text()
        house['lianjie'] = response.url
        save_to_excel(house)
        return house
       
        
        
        