import scrapy
import string
#import urlib.parse.import urljoin

class WikiSpider(scrapy.Spider):
    name = 'gucciMane'
    allowed_domains = ['wikinews.org']
    chars = "ABCDEFGHIJKLMNOPRSTUVWZABCDEFGHIJKLMNOPRSTUVWZ"[35%23:35%23+10]
    start_urls = ['https://en.wikinews.org/wiki/Category:Politics_and_conflicts']
    #start_urls = ['https://en.wikinews.org/w/index.php?title=Category:Politics_and_conflicts&from='+char for char in chars]
    base_url = 'https://en.wikinews.org'
    def parse(self,response):
        for link in response.xpath('/html/body/div[3]/div[3]/div[4]/div[2]/div[2]/div/div/div/ul/li/a/@href').re(r'\/wiki\/[MNOPRSTUW]\S*'):
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_article)
        #print(links)
        
        next_page = response.xpath('/html/body/div[3]/div[3]/div[4]/div[2]/div[2]/a[2]/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        pass
    
    def parse_article(self, response):
        url = response.url
        title = response.xpath('//*[@id="firstHeading"]/text()').get()
        date = response.xpath('/html/body/div[3]/div[3]/div[4]/div/p[1]/strong/text()').get()
        raw_text = response.xpath('/html/body/div[3]/div[3]/div[4]/div/p/descendant::text()').extract() 
        yield {
                "url" : url,
                "title": title,
                "date": date,
                "content": raw_text}


#urlsFromCategory = response.xpath('/html/body/div[3]/div[3]/div[4]/div[2]/div[2]/div/div//a/@href').extract()
#articleURLS = response.xpath('/html/body/div[3]/div[3]/div[4]/div[2]/div[2]/div/div/div/ul/li/a/@href').extract() 