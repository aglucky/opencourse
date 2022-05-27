import scrapy
from scrapy.http.request import Request
from scrapy.loader import ItemLoader
from opencourse.items import berkItem
import re


class berkSpider(scrapy.Spider):
    name = 'berk'
    start_urls = ['https://www2.eecs.berkeley.edu/Scheduling/CS/schedule.html','https://www2.eecs.berkeley.edu/Scheduling/EE/schedule.html']
    domain = 'https://www2.eecs.berkeley.edu'

    def parse(self, response):

        row = '//tr[@class="primary"]'
        numbers = response.xpath(row+'/th[@scope="row"]/a/text()').getall()
        links = response.xpath(row+'/th[@scope="row"]/a/@href').getall()

        for i in range(len(numbers)):
            number = numbers[i]

            link = links[i]
            if not 'http' in link:
                link = self.domain+link

            type = response.xpath(f'(({row})[{i}]/td)[3]/text()').getall()
            name = response.xpath(f'(({row})[{i}]/td)[4]/text()').getall()
            tProf = response.xpath(f'(({row})[{i}]/td)[5]/text()').getall()

            pNames = response.xpath(f'(({row})[{i}]/td)[5]/a/text()').getall()
            pLinks = response.xpath(f'(({row})[{i}]/td)[5]/a/@href').getall()
            for i in range(len(pNames)):
                if not 'http' in pLinks[i]:
                    pLinks[i] = self.domain+pLinks[i]
            profs = {}
            for i in range(len(pNames)):
                profs[pNames[i]] = pLinks[i]

            
            meta = {'name':name,'number':number,'link':link,'number':number,'type':type,'text_profs':tProf,'profs':profs}
            yield Request(link,meta=meta,callback=self.parse_course, dont_filter=True)

    def parse_course(self, response):
        l = ItemLoader(item=berkItem(), response=response)
        l.add_value('name',response.meta['name'])
        l.add_value('number',response.meta['number'])
        l.add_value('link',response.meta['link'])
        l.add_value('type',response.meta['type'])
        l.add_value('text_profs',response.meta['text_profs'])
        l.add_value('profs',response.meta['profs'])

        links=response.xpath('//p/a/@href').getall()
        websites=[]
        for link in links:
            if 'inst' in link:
                websites.append(link)
        l.add_value('websites',websites)

        contentH = response.xpath('//div[@class="content"]/p/strong/text()').getall()
        content = response.xpath('//div[@class="content"]/p/text()').getall()

        for h,c in zip(contentH,content):
            if 'Description' in h:
                l.add_value('description',c)
            elif 'Prerequisites' in h:
                l.add_value('prerequisites',c)
            elif 'Units' in h:
                l.add_value('units',c)
        
        return l.load_item()