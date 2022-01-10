import requests
from bs4 import BeautifulSoup
import json
 
def get_page(url):
    try:
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        res=requests.get(url,headers=headers)
        if res.status_code == 200:
            return res.text
        else:
            return None
    except Exception:
        print('请求失败，请重试')
        return None
def get_info(html):
    #获取电影的排名，电影名，主演，评分，上映时间
    soup=BeautifulSoup(html,'html.parser')
    tables=soup.select('dd')
    #print(tables)
    try:
        for tabel in tables:
            rank=tabel.find(name='i',class_='board-index board-index-1').get_text()
            name=tabel.find(name='p',class_='name').get_text()
            star=tabel.find(name='p',class_='star').get_text().strip()[3:]
            score=tabel.find(name='p',class_='score').get_text()
            time=tabel.find(name='p',class_='releasetime').get_text().strip()[5:]
 
            yield {
                '排名': rank,
                '电影名': name,
                '主演': star,
                '评分': score,
                '上映时间': time
            }
    except  Exception as e:
        print(e)
 
def save_info(text):
    with open('maoyan_info.txt','a',encoding='utf-8')as f:
        f.write(json.dumps(text,ensure_ascii=False)+'\n')
 
if __name__ == '__main__':
    for i in [n*10 for n in range(11)]:
        url='https://maoyan.com/board/4?offset='+str(i)
        html=get_page(url)
        for item in get_info(html):
            print(item)
            save_info(item)
    print('successful!')