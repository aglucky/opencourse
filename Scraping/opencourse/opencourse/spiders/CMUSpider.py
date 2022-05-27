import scrapy
from scrapy.http.request import Request
from scrapy.loader import ItemLoader
from opencourse.items import CMUItem
import pandas as pd
import re


class CMUSpider(scrapy.Spider):
    name = 'CMU'
    start_urls = ['https://csd.cmu.edu/course-profiles/csd-course-list']
    domain = 'https://csd.cmu.edu'

    def parse(self, response):

        rows = response.xpath('//tr').getall()

        for i in range(len(rows)):

            last_offered = response.xpath(f'((//tr)[{i}]/td[@valign="top"])[3]/text()').get()
            number = response.xpath(f'((//tr)[{i}]/td[@valign="top"])[1]/a/text()').get()
            name = response.xpath(f'((//tr)[{i}]/td[@valign="top"])[2]/a/text()').get()
            meta = response.xpath(f'((//tr)[{i}]/td[@valign="top"])[2]/a/@title').get()
            link = response.xpath(f'((//tr)[{i}]/td[@valign="top"])[1]/a/@href').get()
            if number is not None:
                if not 'http' in link:
                    link = self.domain+link

            
                meta = {'name':name,'number':number,'link':link,'meta':meta,'last_offered':last_offered}
                yield Request(link,meta=meta,callback=self.parse_course, dont_filter=True)

    def parse_course(self, response):
        l = ItemLoader(item=CMUItem(), response=response)
        l.add_value('name',response.meta['name'])
        l.add_value('number',response.meta['number'])
        l.add_value('link',response.meta['link'])
        l.add_value('meta',response.meta['meta'])
        l.add_value('last_offered',response.meta['last_offered'])
        l.add_xpath('website', "//a[contains(@title,'course website')]/@href")
        dfs = pd.read_html(response.text)
        df = pd.concat(dfs)

        for j in range(df.shape[0]-1):
            for i in range(df.shape[1]):
                if 'Course Level' in str(df[i][j]):
                    l.add_value('level',df[i][j].split(':')[1].strip())
                elif 'Units' in str(df[i][j]):
                    l.add_value('units',df[i][j].split(':')[1].strip())
                elif 'Special Permission' in str(df[i][j]):
                    l.add_value('permission',str(df[i][j]).split(':')[1].strip())
        
        return l.load_item()