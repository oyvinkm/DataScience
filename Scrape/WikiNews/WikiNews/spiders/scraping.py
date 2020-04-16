import scrapy
import string
#import urlib.parse.import urljoin

class WikiSpider(scrapy.Spider):
    name = 'gucciMane'
    allowed_domains = ['wikinews.org']
    chars = "ABCDEFGHIJKLMNOPRSTUVWZABCDEFGHIJKLMNOPRSTUVWZ"[35%23:35%23+10]
    start_urls = ['https://en.wikinews.org/w/index.php?title=Category:Politics_and_conflicts&from='+char for char in chars]
    def parse(self,response):
        pass


