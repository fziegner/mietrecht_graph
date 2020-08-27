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
    start_urls = ['http://www.jura-basic.de/aufruf.php?file=&find=Mietvertrag']

    def parse(self, response):

        crawled_links = []
        links = list(set(response.xpath('//*[@class="text_inhalt"]/a/@href').getall() + response.xpath('//*[@class="kurzue_links"]/@href').getall()))
        links = [link for link in links if ("jura-basic" and "file=1") in link]

        cleaned_links = []
        for link in links:
            if link.startswith("//"):
                cleaned_links.append("http:" + link)
            else:
                cleaned_links.append(link)

        for link in cleaned_links:
            if link not in crawled_links:
                crawled_links.append(link)
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
