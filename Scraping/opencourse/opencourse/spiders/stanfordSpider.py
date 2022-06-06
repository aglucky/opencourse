import scrapy
from scrapy.http.request import Request
from scrapy.loader import ItemLoader
from opencourse.items import stanfordItem
import re


class stanfordSpider(scrapy.Spider):
    name = 'stanford'
    start_urls = ['https://cs.stanford.edu/courses/schedules/2021-2022.autumn.php']
    domain = 'https://cs.stanford.edu/courses/schedules/2021-2022.autumn.php'

    def parse(self, response):

        links = response.xpath('//td/a/@href').getall()
        numbers = response.xpath('//td/a/text()').getall()
        for i in range(len(links)):
            link = links[i]
            number = numbers[i]
            name = response.xpath(f'((//tr)[{i+1}]/td[@align="left"])[2]/text()').get()
            prof = response.xpath(f'((//tr)[{i+1}]/td[@align="left"])[3]/text()').get()
            meta = {'name':name,'number':number,'link':link,'prof':prof}
            yield Request(link,meta=meta,callback=self.parse_course, dont_filter=True)

    def parse_course(self, response):
        l = ItemLoader(item=stanfordItem(), response=response)
        l.add_value('name',response.meta['name'])
        l.add_value('number',response.meta['number'])
        l.add_value('link',response.meta['link'])
        l.add_value('prof',response.meta['prof'])
        
        return l.load_item()