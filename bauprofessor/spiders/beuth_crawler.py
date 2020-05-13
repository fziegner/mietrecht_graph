import scrapy
import re

class BeuthLexItem(scrapy.Item):
    page_url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    synonym = scrapy.Field()


class BeuthLexSpider(scrapy.Spider):

    name = "BeuthLex"

    start_urls = [
            'https://baulexikon.beuth.de/',
    ]

    def parse(self,response):
        
        links = response.xpath('//a/@href').extract()
        links = [ link for link in links if link.lower().__contains__(".htm") ]

        base_url = 'https://baulexikon.beuth.de/'

        for link in links:
            #absolute_url = self.BASE_URL + link
            if 'list.htm' not in link.lower():
                yield scrapy.Request(base_url + link, callback=self.parseText)
            else:
                yield scrapy.Request(base_url + link, callback=self.parse)

    def parseText(self, response):
        
        element = response.xpath('//div[@class="holder texte"]')

        if len(element) == 1:
            tmp_item = BeuthLexItem()
            tmp_item['page_url'] =  str(response.url)
            tmp_item['title'] = response.xpath('//div[@class="heading"]/h1/text()').extract()[0].strip()
            tmp_item['text'] = response.xpath('//div[@class="holder texte"]/p').extract()
            yield tmp_item
        else:
            print("Nothing to Scrape!")

        #filename = 'quotes-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)