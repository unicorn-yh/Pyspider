from pyspider.libs.base_handler import *
import time
import os
	
class Handler(BaseHandler):    
	crawl_config = {
	}

	def __init__(self):
	    self.base_dir ="D:/yh/YH2021/Python/csdnArch"
	
	@every(minutes=24 * 60)
	def on_start(self):
	    self.crawl('https://www.csdn.net/nav/arch', callback=self.index_page,validate_cert=False)
	
	@config(age=10 * 24 * 60 * 60)
	def index_page(self, response):          
	    for each1 in response.doc('.title h2 a').items():
	            print(each1.text())#标题
	            print(each1.attr("href")+'\n')#链接
	            riqi=time.strftime("%Y-%m-%d")
	            name=each1.text().encode("gbk")
	            lianjie=each1.attr("href")
	            #创建文件夹
	            mk_dir=self.base_dir+"\\"+riqi
	            if not os.path.exists(mk_dir):
	                os.mkdir(mk_dir)
	            #保存文本文件            
	            
	            try:
	                name_file=open(mk_dir+"\\"+name+".txt","w")
	                name_file.write(lianjie)#写入链接
	            except IOError:
	                print("shout")  
	            try:
	                name_file.flush()
	            except ValueError:
	                print("8848")
            name_file.close()