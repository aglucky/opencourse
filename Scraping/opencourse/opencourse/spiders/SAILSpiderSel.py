import scrapy
from scrapy.http.request import Request
from scrapy.loader import ItemLoader
from opencourse.items import SAILItem
from scrapy_selenium import SeleniumRequest

class SAILSpiderSel(scrapy.Spider):
    name = 'SAILSel'
    start_urls = ['https://ai.stanford.edu/courses']
    domain = 'https://ai.stanford.edu'

    script = """
        function main(splash)
            splash.private_mode_enabled = false
            local url = splash.args.url
            assert(splash:go(url))
            assert(splash:wait(10))
            return {
                html = splash:html(),
                png = splash:png(),
                har = splash:har(),
            }
        end
        """

    def start_requests(self): 
        for url in self.start_urls: 
            yield SeleniumRequest(
                url=url, 
                callback=self.parse,
                wait_time=5            
                )

    def parse(self, response):
        links = response.xpath('//div[@class="numbercourse"]/a/@href').getall()
        numbers = response.xpath('//div[@class="numbercourse"]/a/text()').getall()
        names = response.xpath('//a[@class="course-name"]/text()').getall()
        for i in range(len(links)):
            link = links[i]
            number = numbers[i]
            name = names[i]

            pNames = response.xpath(f'(//div[@class="instructorcourse"])[{i}]/a/text()').getall()
            pLinks = response.xpath(f'(//div[@class="instructorcourse"])[{i}]/a/@href').getall()
            profs = {}
            for name, link in zip(pNames, pLinks):
                profs[name] = link


            meta = {'name':name,'number':number,'link':link,'profs':profs}
            yield Request(link,meta=meta,callback=self.parse_course, dont_filter=True)

    def parse_course(self, response):
        l = ItemLoader(item=SAILItem(), response=response)
        l.add_value('name',response.meta['name'])
        l.add_value('number',response.meta['number'])
        l.add_value('link',response.meta['link'])
        l.add_value('profs',response.meta['profs'])
        
        return l.load_item()