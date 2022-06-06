import scrapy
from scrapy.http.request import Request
from scrapy.loader import ItemLoader
from opencourse.items import SAILItem
from scrapy_splash import SplashRequest

class SAILSpiderSplash(scrapy.Spider):
    name = 'SAILSplash'
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
            yield SplashRequest(url, self.parse, 
                endpoint='execute', 
                args={'lua_source': self.script}
           )

    def parse(self, response):
        # links = response.xpath('//div[@class="numbercourse"]/a/@href').getall()
        numbers = response.xpath('//div[@class="numbercourse"]/a/text()').getall()
        names = response.xpath('//a[@class="course-name"]/text()').getall()
        links = response.xpath('//a[@class="course-name"]/@href').getall()
        for i in range(len(links)):
            link = links[i]
            if not 'http' in link:
                link = self.domain + link
            number = numbers[i]
            name = names[i]

            # pNames = response.xpath(f'(//div[@class="instructorcourse"])[{i}]/a/text()').getall()
            profs = response.xpath(f'(//div[@class="instructorcourse"])[{i+1}]/a/@href').getall()
            # profs = {}
            # for name, link in zip(pNames, pLinks):
            #     profs[name] = link

            l = ItemLoader(item=SAILItem(), response=response)
            l.add_value('name',name)
            l.add_value('number',number)
            l.add_value('link',link)
            l.add_value('profs',profs)
        
            yield l.load_item()

        #     meta = {'name':name,'number':number,'link':link,'profs':profs}
        #     yield SplashRequest(link, self.parse_course, meta = meta,
        #         endpoint='execute', 
        #         args={'lua_source': self.script}
        #    )

    def parse_course(self, response):
        l = ItemLoader(item=SAILItem(), response=response)
        l.add_value('name',response.meta['name'])
        l.add_value('number',response.meta['number'])
        l.add_value('link',response.meta['link'])
        l.add_value('profs',response.meta['profs'])
        
        return l.load_item()