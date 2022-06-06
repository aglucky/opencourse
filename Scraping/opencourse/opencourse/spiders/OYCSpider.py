import scrapy
from scrapy.http.request import Request
from scrapy.loader import ItemLoader
from opencourse.items import OYCItem
import re


class OYCSpider(scrapy.Spider):
    name = 'YALE_OYC'
    start_urls = ['https://oyc.yale.edu/courses']
    domain = 'https://oyc.yale.edu'


    def parse(self, response):
        # courses = response.xpath('//ul[@class="courseRow"]')
        department = response.xpath('//td[@class="views-field views-field-title active"]/a/text()').getall()
        number = response.xpath('//td[@class="views-field views-field-field-course-number"]/a/text()').getall()
        name = response.xpath('//td[@class="views-field views-field-title-1"]/a/text()').getall()
        link = response.xpath('//td[@class="views-field views-field-title-1"]/a/@href').getall()
        professor = response.xpath('//td[@class="views-field views-field-field-professors-last-name"]/text()').getall()
        date = response.xpath('//td[@class="views-field views-field-field-semester"]/text()').getall()
        for i in range(len(name)):
            nm = name[i].strip()
            nr = number[i].strip()
            prof = professor[i].strip()
            ln = link[i].strip()
            dt = date[i].strip()

            if not 'http' in ln:
                ln = self.domain+ln
            meta = {'name':nm,'number':nr,'date':dt,'link':ln,'professor':prof}
            yield Request(ln,meta=meta,callback=self.parse_course, dont_filter=True)

    def parse_course(self, response):
        l = ItemLoader(item=OYCItem(), response=response)
        l.add_value('name',response.meta['name'])
        l.add_value('number',response.meta['number'])
        l.add_value('professor',response.meta['professor'])
        l.add_value('link',response.meta['link'])
        l.add_value('date',response.meta['date'])

        description = response.xpath('(//div[@class="field-content"])[3]/descendant-or-self::*/text()').get()
        l.add_value('description',description)
        
        return l.load_item()