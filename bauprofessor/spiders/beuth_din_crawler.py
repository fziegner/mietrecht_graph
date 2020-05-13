import scrapy
import re

class BeuthDINItem(scrapy.Item):
    page_url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    synonym = scrapy.Field()


class BeuthDINSpider(scrapy.Spider):

    name = "Baunormenlexikon"

    start_urls = [
            'https://www.baunormenlexikon.de/',
    ]

    def parse(self,response):
        
        links = response.xpath('//a/@href').extract()
        links = [ link for link in links if link.lower().__contains__(".htm") ]

        base_url = 'https://www.baunormenlexikon.de/'

        #kategorien
        #index
        #/vob-c-2019/

        
        for link in links:

            if link.__contains__("norm"):
                # Do the thing
                print()
            elif link.__contains__(""):
                # Do the other thing
                print()
            elif link.__contains__(""):
                # Fall-through by not using elif, but now the default case includes case 'a'!
                print()
            elif link.__contains__(""):
                # Do yet another thing
                print()
            else:
            # Do the default
                print()
            #absolute_url = self.BASE_URL + link
            if 'list.htm' not in link.lower():
                yield scrapy.Request(base_url + link, callback=self.parseText)
            else:
                yield scrapy.Request(base_url + link, callback=self.parse)

    def parseItem(self, response):
        
        element = response.xpath('//div[@class="holder texte"]')

        if len(element) == 1:
            tmp_item = BeuthDINItem()
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

    def parseDIN(self, response):
        print()

    def parseVOB(self, response):
        print()