import scrapy
import re

class BMGEVItem(scrapy.Item):
    page_url = scrapy.Field()
    title = scrapy.Field()
    sub_title = scrapy.Field()
    text = scrapy.Field()
    crosslinks = scrapy.Field()

class BMGEVSpider(scrapy.Spider):

    name = "BMGEV"
    start_urls = ['https://www.bmgev.de/mietrecht/tipps-a-z/index/a/']

    def parse(self, response):

        links = response.xpath("//*[@class='news-header-list-container']//@href").getall()

        cleaned_links = []
        for link in links:
            if link.startswith("mietrecht"):
                cleaned_links.append("https://www.bmgev.de/" + link)

        for link in cleaned_links:
            if 'artikel' in link:
                yield scrapy.Request(link, callback=self.parseText)
            else:
                yield scrapy.Request(link, callback=self.parse)

    def parseText(self, response):

        element = response.xpath("//*[@class='news-single-item']")

        if len(element) == 1:
            tmp_item = BMGEVItem()
            tmp_item['page_url'] =  str(response.url)
            tmp_item['title'] = response.xpath("string(//*[@class='news-single-item']/h1)").get()
            tmp_item['sub_title'] = response.xpath("string(//*[@class='news-single-subheader'])").get()
            if(tmp_item['sub_title'] and response.xpath("//*[@class='news-single-related']").get()):
                tmp_item['text'] = re.sub("[\n\r\t]","",response.xpath("string(//*[@class='news-single-item'])").get()).split("Zurück")[0].split("in Verbindung")[0].split(tmp_item['sub_title'],1)[1].strip()
            elif(response.xpath("//*[@class='news-single-related']").get()):
                tmp_item['text'] = re.sub("[\n\r\t]","",response.xpath("string(//*[@class='news-single-item'])").get()).split("Zurück")[0].split("in Verbindung")[0].split(tmp_item['title'],1)[1].strip()
            else:
                tmp_item['text'] = re.sub("[\n\r\t]","",response.xpath("string(//*[@class='news-single-item'])").get()).split("Zurück")[0].split(tmp_item['title'],1)[1].strip()
            tmp_item['crosslinks'] = response.xpath("//*[@class='news-single-item']//a/@href[not(ancestor::div/@class='news-single-backlink' or ancestor::div/@class='news-single-additional-info')]").getall()
            yield tmp_item
        else:
            print("Nothing to Scrape!")
