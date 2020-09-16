import scrapy
import re

class MietrechtLexikonItem(scrapy.Item):
    page_url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    crosslinks = scrapy.Field()

class MietrechtLexikonSpider(scrapy.Spider):

    name = "MietrechtLexikon"
    start_urls = ['http://www.mietrechtslexikon.de/a1lexikon2/katalog_neu.htm']

    def parse(self, response):

        links = response.xpath('//a/@href').extract()
        links = [link for link in links if link.__contains__("lexikon")]

        for link in links:
            if 'katalog' in link:
                yield scrapy.Request(link, callback=self.parse)
            else:
                yield scrapy.Request(link, callback=self.parseText)

    def parseText(self, response):

        element = response.xpath('//*[@id="Content"]')

        if len(element) == 1:
            tmp_item = MietrechtLexikonItem()
            url = str(response.url)
            if url.startswith("https"):
                tmp_item['page_url'] =  str(response.url).replace("https","http")
            else:
                tmp_item['page_url'] =  str(response.url)
            tmp_item['title'] = response.xpath('//*[@class="column one"]/h1/text()').get()
            sub_title = response.xpath('string(//*[@class="the_content_wrapper"]/h2)').get()
            if sub_title:
                if(response.xpath('//*[@class="toc_title"]/text()').get()):
                    tmp_item['text'] = sub_title + " " + response.xpath('string(//*[@class="the_content_wrapper"])').get().split(sub_title)[2]
                else:
                    tmp_item['text'] = sub_title + " " + response.xpath('string(//*[@class="the_content_wrapper"])').get().split(sub_title)[1]
            else:
                tmp_item['text'] = response.xpath('string(//*[@class="the_content_wrapper"])').get()
            tmp_item['crosslinks'] = response.xpath('//*[@class="the_content_wrapper"]/*[@class="schriften"]/a/@href').extract()
            yield tmp_item
        else:
            print("Nothing to Scrape!")

        #filename = 'quotes-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)
