import scrapy
import re

class HausberaterItem(scrapy.Item):
    page_url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    synonym = scrapy.Field()


class HausberaterSpider(scrapy.Spider):

    name = "Hausberater"

    start_urls = [
            'https://www.hausbauberater.de/fachbegriffe',
    ]





    def parse(self,response):
        
        links = response.xpath('//a/@href').extract()
        links = [ link for link in links if link.__contains__("fachbegriffe") ]

        base_url = 'https://www.hausbauberater.de'

        for link in links:
            #absolute_url = self.BASE_URL + link
            if re.search("/fachbegriffe/[a-z0-9\\-]{3,}",link) is not None:
                yield scrapy.Request(base_url + link, callback=self.parseText)
            else:
                yield scrapy.Request(base_url + link, callback=self.parse, )

    def parseText(self, response):
        
        element = response.xpath('//*[@class="row1"]')

        if len(element) == 1:
            tmp_item = HausberaterItem()
            tmp_item['page_url'] =  str(response.url)
            tmp_item['title'] = response.xpath('//tr[@class="row1"]/td/a/text()').extract()[0].strip()
            tmp_item['text'] = response.xpath('//tr[@class="row1"]/td//p').extract()
            tmp_item['synonym'] = response.xpath('//tr[@class="row1"]/td/text()').extract()
            yield tmp_item
        else:
            print("Nothing to Scrape!")

        #filename = 'quotes-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)