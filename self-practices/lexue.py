from pyspider.libs.base_handler import *

DIR_PATH = 'D:/yh/YH2021/Java/test'   #资源保存路径
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    'Host' : 'lexue.bit.edu.cn',
    'Upgrade-Insecure-Requests' : '1'
} 
 
class Handler(BaseHandler):
    crawl_config = {
    }
 
    def __init__(self):
        self.base_url = 'https://lexue.bit.edu.cn/mod/folder/view.php?id=294299'
        self.deal = Deal()
 
    def on_start(self):
        self.crawl(self.base_url, callback=self.index_page, validate_cert=False)
 
    def index_page(self, response):
        session = requests.Session()
        session.max_redirects = 5
        try:
            r = session.post(url, headers=headers, params=querystring, data=payload)
        except requests.exceptions.TooManyRedirects as exc:
            r = exc.response
        dir_path = self.deal.mkDir("lexue")
        for each in (response.doc('[div="ygtvchildren"]'))('a[href^="http"]').items():
            if dir_path:
                self.crawl(each.attr.href, callback=self.save_img, save={'dir_path': dir_path},validate_cert=False)
 
    def save_img(self, response):
        content = response.content
        dir_path = response.save['dir_path']
        file_name = response.save['file_name']
        file_path = dir_path + '/' + file_name
 
import os
 
class Deal:
    def __init__(self):
        self.path = DIR_PATH             #DIR_PATH: 资源保存路径
        if not self.path.endswith('/'):
            self.path = self.path + '/'
        if not os.path.exists(self.path):
            os.makedirs(self.path)
 
    def mkDir(self, path):               #创建 MM 名字对应的文件夹
        path = path.strip()
        dir_path = self.path + path
        exists = os.path.exists(dir_path)
        if not exists:
            os.makedirs(dir_path)
            return dir_path
        else:
            return dir_path