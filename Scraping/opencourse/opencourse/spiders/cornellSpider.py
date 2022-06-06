import scrapy
from scrapy.http.request import Request
from scrapy.loader import ItemLoader
from opencourse.items import cornellItem
import re


class berkSpider(scrapy.Spider):
    name = 'cornell'
    start_urls = ['https://www.cs.cornell.edu/courseinfo/listofcscourses']
    domain = 'https://www.cs.cornell.edu'

    def parse(self, response):

        names = response.xpath('//li[@class="cs-course"]/strong//descendant-or-self::*/text()').getall()

        for i in range(len(names)):
            name = names[i]

            links = response.xpath(f'(//li[@class="cs-course"])[{i+1}]/ul/li/a/@href').getall()
            texts = response.xpath(f'(//li[@class="cs-course"])[{i+1}]/ul/li/a/text()').getall()
            sites = {}
            for link,text in zip(links,texts):
                sites[text] = link

            l = ItemLoader(item=cornellItem(), response=response)
            l.add_value('name', name)
            l.add_value('sites', sites)
            yield l.load_item()
            
        
