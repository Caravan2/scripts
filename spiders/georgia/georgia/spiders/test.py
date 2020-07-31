import scrapy

class MySpider(scrapy.Spider):
    name = 'example.com'
    allowed_domains = ['hr.ge']
    start_urls = [
        'http://www.hr.ge/1.html',
        'http://www.hr.ge/2.html',
        'http://www.hr.ge/3.html',
    ]

    def parse(self, response):
        for h3 in response.xpath('//h3').getall():
            yield {"title": h3}

        for href in response.xpath('//a/@href').getall():
            yield scrapy.Request(response.urljoin(href), self.parse)