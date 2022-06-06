import scrapy
from scrapy.http.request import Request
from scrapy.loader import ItemLoader
from opencourse.items import OCWItem
import re


class OCWSpider(scrapy.Spider):
    name = 'MIT_OCW'
    start_urls = ['https://ocw.mit.edu/courses/']
    domain = 'https://ocw.mit.edu'


    def parse(self, response):
        # courses = response.xpath('//ul[@class="courseRow"]')
        name = response.xpath('//h4[@class="course_title"]/a/text()').getall()
        number = response.xpath('//li[@class="courseNumCol"]/a/text()').getall()
        level = response.xpath('//li[@class="courseLevelCol"]/a/text()').getall()
        link = response.xpath('//h4[@class="course_title"]/a/@href').getall()
        for i in range(len(name)):
            nm = name[i].strip()
            nr = number[i].strip()
            lv = level[i].strip()
            ln = link[i].strip()

            if not 'http' in ln:
                ln = self.domain+ln
            meta = {'name':nm,'number':nr,'level':lv,'link':ln}
            yield Request(ln,meta=meta,callback=self.parse_course, dont_filter=True)

    def parse_course(self, response):
        l = ItemLoader(item=OCWItem(), response=response)
        l.add_value('name',response.meta['name'])
        l.add_value('number',response.meta['number'])
        l.add_value('level',response.meta['level'])
        l.add_value('link',response.meta['link'])
        l.add_xpath('taught_in','//p[@itemprop="startDate"]/text()')
        description = response.xpath('//div[@id="description"]/div/p/descendant-or-self::*/text()').getall()
        description = ' '.join(description)
        l.add_value('description',description)
        features = response.xpath('//ul[@class="specialfeatures"]/li/a/text()').getall()
        l.add_value('features',features)
        return l.load_item()