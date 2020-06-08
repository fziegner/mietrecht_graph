import scrapy
import json
class Anlage(scrapy.Item):
    type = scrapy.Field()
    page_url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    doc_title = scrapy.Field()
    honorar = scrapy.Field()
    previous = scrapy.Field()
    next = scrapy.Field()

class LP(scrapy.Item):
    type=scrapy.Field()
    page_url= scrapy.Field()
    paragraph= scrapy.Field()
    text= scrapy.Field()
    title= scrapy.Field()
    previous = scrapy.Field()
    next = scrapy.Field()
    laws=scrapy.Field()
    crosslinks = scrapy.Field()


class HOAISpider(scrapy.Spider):
    name = "HOAI"
    start_urls = ['https://dejure.org/gesetze/HOAI']
    base_url = "https://dejure.org"

    def parse(self,response):
        
        links = [ link for link in response.xpath('//a/@href').extract() if link.lower().__contains__(".htm") and "HOAI" in link]
        print("links: ", links)
        
        for link in links:
            if "Anlage" in link:
                yield scrapy.Request(self.base_url +link, callback=self.parseAnlage)
            else:
                yield scrapy.Request(self.base_url +link, callback=self.parseItem)

    def parseItem(self, response):
        
        # element = response.xpath('//table[@class="doc header"]')
        print(str(response.url))
        tmp_item = LP()
        tmp_item["type"] = "LP"
        tmp_item['page_url'] = str(response.url)
        tmp_item["title"] = " ".join(response.xpath('//h1[@class="normueberschrift"]/text()').extract())
        tmp_item['paragraph'] =" ".join([x.xpath("string()").getall()[0].strip() for x in response.xpath('//div[@class="headgesetz clearfix"]/child::*[not(@class="hideprint")]')])

        tmp_item["laws"] =list(set(
            [self.base_url + y for x in response.xpath('//div[@id="gesetzestext"]/child::*').xpath("a/@href") for y in x.getall() if "gesetze" in y]
        ))
        tmp_item["crosslinks"] = list(set(
            [self.base_url + x for x in response.xpath(
                '//div[@class="content_inner" and h2[contains(text(), "Querverweise")]]/descendant::a/@href').getall()]
        ))

        try:
            tmp_item['text'] = [x.xpath('string()').getall()[0] for x in response.xpath('//div[@id="gesetzestext"]/child::*')]
            tmp_item['text'] = " ".join(tmp_item['text'] )
        except:
            try:
                tmp_item['text'] = [x.xpath('string()').getall()for x in response.xpath('//div[@id="gesetzestext"]/child::*')]
                tmp_item['text'] = " ".join(tmp_item['text'])
            except:
                pass
        try:
            tmp_item["previous"] = self.base_url + response.xpath('//div[@class="pfeileoben"]/a/@href').extract()[0]
        except: pass

        try:
            tmp_item["next"] = self.base_url + response.xpath('//div[@class="pfeileoben"]/a/@href').extract()[1]
        except: pass

        yield tmp_item

    def parseAnlage(self, response):
        content = [x for x in response.xpath('//div[@class="gesetzestext clearfix"]/child::*')]
        tmp_item = Anlage()
        tmp_item["type"] = "Anlage"
        try: tmp_item["page_url"] = response.url
        except: pass

        tmp_item['title'] = content[0].xpath("string()").getall()[0].replace("\n"," ").replace("\t"," ")
        tmp_item['doc_title'] = content[1].xpath("string()").getall()[0].replace("\n"," ").replace("\t"," ")
        tmp_item['text'] = content[2].xpath("string()")[0]
        try:
            table = [x.xpath("node()").xpath("td/text()").getall() for x in content[4:]]
            tmp_item['honorar'] = json.dumps([x for x in table if x != [' ']])
        except: pass

        try:
            tmp_item["previous"] = self.base_url + response.xpath('//div[@class="pfeileoben"]/a/@href').extract()[0]
        except:
            pass

        try:
            tmp_item["next"] = self.base_url + response.xpath('//div[@class="pfeileoben"]/a/@href').extract()[1]
        except:
            pass
        yield tmp_item
