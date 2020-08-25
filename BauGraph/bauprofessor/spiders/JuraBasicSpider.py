import scrapy
import re

class JuraBasicItem(scrapy.Item):
    page_url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    crosslinks = scrapy.Field()
    category = scrapy.Field()

class JuraBasicSpider(scrapy.Spider):

    name = "JuraBasic"
    start_urls = ['http://lexikon.jura-basic.de/aufruf.php?file=1&find=Mietvertrag',]

    def parse(self, response):

        links = response.xpath('//a/@href').extract()
        links = [link for link in links if link.__contains__("file=1")]

        for link in links:
            if 'Mietvertrag' in link:
                yield scrapy.Request(link, callback=self.parse)
            else:
                yield scrapy.Request(link, callback=self.parseText)

    def parseText(self, response):

        element = response.xpath('//*[@class="text_titel"]')

        if len(element) == 1:
            tmp_item = JuraBasicItem()
            tmp_item['page_url'] =  str(response.url)
            tmp_item['title'] = response.xpath('//*[@class="text_titel"]/text()').get().strip() + " - " + response.xpath('//*[@class="text_inhalt"]/h2/text()').get().strip()
            tmp_item['text'] = re.sub("[\r]","",response.xpath('string(//*[@class="text_inhalt"])').get()).strip()
            tmp_item['crosslinks'] = set(response.xpath('//*[@class="text_inhalt"]/a/@href').extract())
            tmp_item['category'] = response.xpath('//*[@class="text_titel"]/text()').get()
            yield tmp_item
        else:
            print("Nothing to Scrape!")

        #filename = 'quotes-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)
