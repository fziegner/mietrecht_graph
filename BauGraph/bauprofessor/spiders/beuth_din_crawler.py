import scrapy
import re

class BeuthDINItem(scrapy.Item):
    page_url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    related = scrapy.Field()
    norm = scrapy.Field()
    key_phrases = scrapy.Field()
    # synonym = scrapy.Field()


class BeuthDINSpider(scrapy.Spider):
    name = "BaunormenlexikonDIN"
    def start_requests(self):
        urls = ['https://www.baunormenlexikon.de/deutsche-norm/8ad1cdbb-afa2-4cb6-8181-34f24cd5a448']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
        
        links = response.xpath('//a/@href').extract()
        links = [ link for link in links if link.lower().__contains__("/norm/") ]

        base_url = 'https://www.baunormenlexikon.de/'

        #kategorien
        #index
        #/vob-c-2019/
        print("links: ", links)
        
        for link in links:
            yield scrapy.Request(link, callback=self.parseItem)

    def parseItem(self, response):
        
        # element = response.xpath('//table[@class="doc header"]')
        print(str(response.url))
        tmp_item = BeuthDINItem()
        tmp_item['page_url'] =  str(response.url)
        tmp_item['title'] = response.xpath('//td[@class="doc-label"]/h1/text()').getall()[0].split("|")[0].strip()
        tmp_item['text'] = response.xpath('//div[@class="lh14 doc-lecture"]/div/div[@class="mB_m "]/span/text()').getall()
        tmp_item['related'] = response.xpath('//ul[@class="doc-related lh14"]/li/div/a/@href').extract()
        tmp_item["norm"] = "DIN"
        tmp_item["key_phrases"] = [(x.xpath('@href').extract()[0] ,x.xpath('text()').extract()[0] )for x in response.xpath('//div[@class="padding descriptors"]/a')]
        yield tmp_item


        #filename = 'quotes-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)

    def parseDIN(self, response):
        print()

    def parseVOB(self, response):
        print()