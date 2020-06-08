import scrapy
import re

class BauprofessorItem(scrapy.Item):
    page_url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    related_term = scrapy.Field()
    category = scrapy.Field()
    keywords = scrapy.Field()
    crosslinks = scrapy.Field()


class BauprofessorSpider(scrapy.Spider):

    name = "Bauprofessor"

    start_urls = [
            'https://www.bauprofessor.de/lexikon/a/0',
    ]





    def parse(self,response):
        
        links = response.xpath('//a/@href').extract()
        links = [ link for link in links if link.__contains__("https://www.bauprofessor.de/") ]

        for link in links:
            #absolute_url = self.BASE_URL + link
            if 'lexikon' in link:
                yield scrapy.Request(link, callback=self.parse, )
            else:
                yield scrapy.Request(link, callback=self.parseText)

    def parseText(self, response):
        
        element = response.xpath('//*[@class="topic"]')

        if len(element) == 1:
            tmp_item = BauprofessorItem()
            tmp_item['page_url'] =  str(response.url)
            tmp_item['title'] = response.xpath('//*[@class="topic"]/div/h1/text()').extract()[0]
            tmp_item['text'] = re.sub("[\r\n]","",response.xpath('string(//div[@id="panelDefinition"])').extract()[0]).strip()
            tmp_item['crosslinks'] = response.xpath('//div[@id="panelDefinition"]//a/@href').extract()
            tmp_item['related_term'] = response.xpath('//div[@id="pnlOtherBegriffe"]//article/div/a/@href').extract()
            tmp_item['category'] = response.xpath('//div[@class="article__rubric"]/text()').extract()[0]
            tmp_item['keywords'] = response.xpath('//div[@class="topic-keywords"]/a/text()').extract()
            yield tmp_item
        else:
            print("Nothing to Scrape!")

        #filename = 'quotes-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)