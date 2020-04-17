import scrapy
import string
#import urlib.parse.import urljoin

class WikiSpider(scrapy.Spider):
    name = 'gucciMane'
    allowed_domains = ['wikinews.org']
    chars = "ABCDEFGHIJKLMNOPRSTUVWZABCDEFGHIJKLMNOPRSTUVWZ"[35%23:35%23+10]
    start_urls = ['https://en.wikinews.org/w/index.php?title=Category:Politics_and_conflicts&from='+char for char in chars]
    base_url = 'https://en.wikinews.org'
    links = []
    def parse(self,response):
        links = response.xpath('/html/body/div[3]/div[3]/div[4]/div[2]/div[1]/div/div/div[1]/ul//a/@href').extract()
        for link in links:
            newlink = str(self.base_url + link)
        pass


urlsFromCategory = response.xpath('/html/body/div[3]/div[3]/div[4]/div[2]/div[2]/div/div//a/@href').extract()