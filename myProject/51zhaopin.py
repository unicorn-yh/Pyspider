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
 
class Handler(BaseHandler):
    crawl_config = {
    }

    '''def get_city_code():
        url = 'https://js.51jobcdn.com/in/js/h5/dd/d_jobarea.js?20191212'
        r = requests.get(url)
        begin = r.text.find('var hotcity')
        if begin == -1:
            print('Not find var hotcity')
        # print(begin)
        end = r.text.find(';',begin)
        if end == -1:
            print('Not find ; ')
        # print(end)
        result_text = r.text[begin : end-1]
        #print(result_text)
        begin = result_text.find('{')
        city_dict_str = result_text[begin:]
        # print(city_dict_str)
        key,value = "",""
        key_list,value_list = [],[]
        count = 1
        i = 0
        while i < len(city_dict_str):
            if city_dict_str[i] == '"' and count == 1:
                count = 2
                i += 1
                while city_dict_str[i] != '"':
                    key += city_dict_str[i]
                    i += 1
                key_list.append(key)
                key = ""
                i += 1
            if city_dict_str[i] == '"' and count == 2:
                count = 1
                i += 1
                while city_dict_str[i] != '"':
                    value += city_dict_str[i]
                    i += 1
                value_list.append(value)
                value = ""
                i += 1
            i += 1
        city_dict = {}
        i = 0
        while i < len(key_list):
            city_dict[value_list[i]] = key_list[i]
            i += 1
        # print(city_dict)
        return city_dict'''

    # 获取职位总页数
    '''def get_pageNumber():
        url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,'+key+',2,1.html'
        r = requests.get(url=url,headers=headers)
        soup = BeautifulSoup(r.content.decode('gbk'),'html5lib')
        find_page = soup.find('div',class_='rt').getText()
        temp = re.findall(r"\d+\.?\d*",find_page)
        if temp:
            pageNumber = math.ceil(int(temp[0])/50)
            return pageNumber
        else:
            return 0'''

    def __init__(self):
        '''url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,'+key+',2,1.html'
        r = requests.get(url=url,headers=headers)
        soup = BeautifulSoup(r.content.decode('gbk'),'html5lib')
        find_page = soup.find('div',class_='rt').get_text()
        temp = re.findall(r"\d+\.?\d*",find_page)
        if temp:
            pageNumber = math.ceil(int(temp[0])/50)
        else:
            pageNumber = 0'''
        self.urls=[]
        for page in range(1,10):
            url ='http://search.51job.com/list/000000,000000,0000,00,9,99,'+key+',2,'+str(page)+'.html'
            self.urls.append(url)
    
    @every(minutes=24 * 60)
    def on_start(self):
        for url in self.urls:
            self.crawl(url,callback=self.index_page,validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):   #下一页
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page,validate_cert=False)
        #抓取内容页
        '''url = response.doc('#pageNum > a:nth-last-child(2)').attr.href
        if url:
            self.crawl(url, callback=self.index_page,validate_cert=False) 
        #next = response.doc('#FILTERED_LIST > div.al_border.deckTools.btm > div > div > a').attr.href
        #self.crawl(next,callback=self.index_page,validate_cert=False)'''

    @config(priority=2)
    def detail_page(self, response):
        soup = BeautifulSoup(response.text, 'html5lib')
        item['zhiwei'] = soup.find('h1').get_text().replace('\xa0', '')
        item['gongsi'] = soup.find('p', class_='cname').find('a', target='_blank').get_text().replace('\xa0', '')
        item['didian'] = soup.find('span', class_='lname').get_text().replace('\xa0', '')
        item['xinzi'] = soup.find('div', class_='cn').find('strong').get_text().replace('\xa0', '')
        gongsixinxi = soup.find('p', class_='msg ltype').get_text().replace('\t', '').replace('\r', '').replace('\n', '').replace('\xa0', '')
        item['gongsileixing'] = gongsixinxi.split('|')[0]
        item['guimo'] = gongsixinxi.split('|')[1]
        item['hangye'] = gongsixinxi.split('|')[2]
        zhaopinyaoqiu = soup.find('div', class_='t1').get_text().replace('\xa0', '')
        item['jingyan'] = zhaopinyaoqiu.split('\n')[1]
        try:
            item['xueli'] = re.findall(r'<em class="i2"></em>(.*?)</span>', response.text)[0]
        except:
            item['xueli'] = '无'
        try:
            item['fuli'] = soup.find('p', class_='t2').get_text().replace('\n', ' ').replace('\xa0', '')
        except:
            item['fuli'] = '无'
        item['zhiweiyaoqiu'] = re.findall(r'<div class="bmsg job_msg inbox">(.*?)<div class="mt10">', response.text, re.I|re.S|re.M)[0]\
            .replace('\r', '').replace('\n', '').replace('\t', '').replace('\xa0', '').replace('<br>', '')\
            .replace('<br/>', '').replace('<P>', '').replace('</P>', '').replace('?', ' ').replace('<p>', '').replace('</p>', '')\
            .replace('<div>', '').replace('</div>', '').replace('<BR>', '').replace('</BR>', '')
        item['lianjie'] = response.meta['url']
        yield item


    '''@config(priority=2)
    def detail_page(self, response):
        return {
            "职位": 
            "公司":
            "地点":
            "薪资"：
            "公司类型":
            "规模":
            "行业":
            "经验":
            "学历":
            "福利"：
            "职位要求":
            "链接":
        }
        '''