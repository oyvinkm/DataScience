import scrapy
import string

def extract_article(response):
    title = response.xpath('//*[@id="firstHeading"]/text()').extract()
    date = response.xpath('/html/body/div[3]/div[3]/div[4]/div/p[1]/strong/text()').extract()
    raw_text = response.xpath('/html/body/div[3]/div[3]/div[4]/div/p/text()').extract()
    
