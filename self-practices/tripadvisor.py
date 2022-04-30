from pyspider.libs.base_handler import *
import pymongo

class Handler(BaseHandler):
    crawl_config = {
    }
    client = pymongo.MongoClient('localhost')
    db = client['trip']


    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.tripadvisor.cn/Attractions-g186338-Activities-London_England.html', callback=self.index_page,validate_cert=False)


    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page,validate_cert=False)
            
        next = response.doc('#FILTERED_LIST > div.al_border.deckTools.btm > div > div > a').attr.href
        self.crawl(next,callback=self.index_page,validate_cert=False)
    
    @config(priority=2)
    def detail_page(self, response):
        name = response.doc('#HEADING').text()
        rating = response.doc('#taplc_location_detail_overview_attraction_0 > div > div.overviewContent > div.ui_columns.is-multiline.is-mobile.reviewsAndDetails > div.ui_column.is-6.reviews > div.rating > span').text()
        address = response.doc('#taplc_attraction_detail_listing_0 > div.section.location > div.detail_section.address').text()
        return {
            "url": response.url,
            "title": response.doc('title').text(),
            "name":name,
            "rating":rating,
            "address":address,
        }
    def on_result(self,result):
        if result:
            self.save_to_mongo(result)
    
    def save_to_mongo(self,result):
        if self.db['london'].insert(result):
            print('successfully',result)