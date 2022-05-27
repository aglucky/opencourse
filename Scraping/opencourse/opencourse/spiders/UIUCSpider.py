import scrapy
from scrapy.http.request import Request
from scrapy.loader import ItemLoader
from opencourse.items import UIUCItem
import re


class OYCSpider(scrapy.Spider):
    name = 'UIUC'
    start_urls = ['https://cs.illinois.edu/academics/courses']
    domain = 'https://cs.illinois.edu'

    def parse(self, response):
        # courses = response.xpath('//ul[@class="courseRow"]')
        number = response.xpath('//td[@class="rubric"]/a/text()').getall()
        name = response.xpath('//td[@class="title"]/a/text()').getall()
        link = response.xpath('//td[@class="title"]/a/@href').getall()
        website = response.xpath('//td[@class="website"]/a/@href').getall()
        for i in range(len(name)):
            nm = name[i].strip()
            nr = number[i].strip()
            ln = link[i].strip()
            site = website[i].strip()
            pr = response.xpath(f'(//tr){[i+1]}/td[@class="prereqs"]/descendant-or-self::*/text()').getall()
            pr = ''.join(pr)

            if not 'http' in ln:
                ln = self.domain+ln
            meta = {'name':nm,'number':nr,'link':ln,'website':site,'prereq':pr}
            yield Request(ln,meta=meta,callback=self.parse_course, dont_filter=True)

    def parse_course(self, response):
        l = ItemLoader(item=UIUCItem(), response=response)
        l.add_value('name',response.meta['name'])
        l.add_value('number',response.meta['number'])
        l.add_value('link',response.meta['link'])
        l.add_value('website',response.meta['website'])
        l.add_value('prereq',response.meta['prereq'])

        l.add_xpath('description', '//div[@id="extCoursesDescription"]/div[@class="extCoursesProfileContent"]/text()')
        l.add_xpath('last_updated', '//div[@id="extCoursesLastUpdated"]/div[@class="extCoursesProfileContent"]/text()')

        dNames = response.xpath('//div[@id="extCoursesDirectors"]/div/a/text()').getall()
        dLinks = response.xpath('//div[@id="extCoursesDirectors"]/div/a/@href').getall()
        for i in range(len(dNames)):
            if not 'http' in dLinks[i]:
                dLinks[i] = self.domain+dLinks[i]
        directors = {}
        for i in range(len(dNames)):
            directors[dNames[i]] = dLinks[i]
        l.add_value('directors',directors)
        
        return l.load_item()