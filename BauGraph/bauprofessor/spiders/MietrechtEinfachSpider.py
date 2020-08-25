import scrapy
import re

class MietrechtEinfachItem(scrapy.Item):
    page_url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    crosslinks = scrapy.Field()

class MietrechtEinfachSpider(scrapy.Spider):

    name = "MietrechtEinfach"
    start_urls = ['http://www.mietrecht-einfach.de/mietrecht-lexikon.html',]

    def parse(self, response):

        links = set(response.xpath('//*[@id="right"]/a/@href').getall())

        for link in links:
            if 'mietrecht' in link:
                yield scrapy.Request(link, callback=self.parse)
            else:
                yield scrapy.Request(link, callback=self.parseText)

    def parseText(self, response):

        element = response.xpath('//*[@id="right"]')

        if len(element) == 1:
            tmp_item = MietrechtEinfachItem()
            tmp_item['page_url'] =  str(response.url)
            tmp_item['title'] = response.xpath('//*[@id="right"]/h2/text()').get()
            text = re.sub("[\n\r\t]","",response.xpath('string(//*[@id="right"])').get())
            text = re.sub("<.*?\>","",text) #delete all strings between angle brackets
            tmp_item['text'] = text.split(title,1)[1].split("Zurück zum Mietrecht")[0]
            tmp_item['crosslinks'] = set(response.xpath('//*[@id="right"]/a/@href').getall())
            yield tmp_item
        else:
            print("Nothing to Scrape!")

        #filename = 'quotes-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)
