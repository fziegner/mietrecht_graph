import scrapy
import re

class JuraBasicItem(scrapy.Item):
    page_url = scrapy.Field()
    title = scrapy.Field()
    sub_title = scrapy.Field()
    text = scrapy.Field()
    crosslinks = scrapy.Field()
    category = scrapy.Field()

class JuraBasicSpider(scrapy.Spider):

    name = "JuraBasic"
    start_urls = ['http://www.jura-basic.de/aufruf.php?file=&pp=&art=6&find=t_1468yxymietrecht',
                     'http://www.jura-basic.de/aufruf.php?file=&pp=&art=6&find=t_1488yxymietrecht',
                     'http://www.jura-basic.de/aufruf.php?file=&pp=&art=6&find=t_742yxymietrecht',
                     'http://www.jura-basic.de/aufruf.php?file=&pp=&art=6&find=t_1067yxymietrecht',
                     'http://www.jura-basic.de/aufruf.php?file=&pp=&art=6&find=t_1066yxymietrecht',
                     'http://www.jura-basic.de/aufruf.php?file=&pp=&art=6&find=t_698yxymietrecht',
                     'http://www.jura-basic.de/aufruf.php?file=&pp=&art=6&find=t_1446yxymietrecht',
                     'http://www.jura-basic.de/aufruf.php?file=&pp=&art=6&find=t_1145yxymietrecht',
                     'http://www.jura-basic.de/aufruf.php?file=&pp=&art=6&find=t_219yxymietrecht',
                     'http://www.jura-basic.de/aufruf.php?file=&pp=&art=6&find=t_1663yxymietrecht',
                     'http://www.jura-basic.de/aufruf.php?file=&pp=&art=6&find=t_1525yxymietrecht',
                     'http://www.jura-basic.de/aufruf.php?file=&pp=&art=6&find=t_611yxymietrecht',
                     'http://www.jura-basic.de/aufruf.php?file=&pp=&art=6&find=t_89yxymietrecht']
    custom_settings = {
        'DEPTH_LIMIT': 2
    }

    def parse(self, response):

        links = list(set(response.xpath('//*[@class="text_inhalt"]/a/@href').getall() + response.xpath('//*[@class="kurzue_links"]/@href').getall()))
        links = [link for link in links if ("jura-basic" and "file=1") in link]

        cleaned_links = []
        for link in links:
            if link.startswith("//"):
                cleaned_links.append("http:" + link)
            else:
                cleaned_links.append(link)

        element = response.xpath('//*[@class="text_titel"]')

        if len(element) == 1 and (str(response.url) not in JuraBasicSpider.start_urls):
            tmp_item = JuraBasicItem()
            tmp_item['page_url'] =  str(response.url)
            tmp_item['title'] = response.xpath('//*[@class="text_titel"]/text()').get().strip()
            if(response.xpath('//*[@class="text_inhalt"]/h2/text()').get()):
                tmp_item['sub_title'] = response.xpath('//*[@class="text_inhalt"]/h2/text()').get().strip()
            if "sub_title" in tmp_item:
                tmp = re.sub("[\r]","",response.xpath('string(//*[@class="text_inhalt"])').get()).strip()
                tmp_item['text'] = re.split("(<< )?(\|\| *)?(Rz. [0-9][0-9]?)",tmp)[4].strip()
            else:
                tmp_item['text'] = re.sub("[\r]","",response.xpath('string(//*[@class="text_inhalt"])').get()).strip()
            crosslinks = list(set(response.xpath('//*[@class="text_inhalt"]/a/@href').getall()))
            cleaned_crosslinks = []
            for link in crosslinks:
                if link.startswith("//"):
                    cleaned_crosslinks.append("http:" + link)
                else:
                    cleaned_crosslinks.append(link)
            tmp_item['crosslinks'] = cleaned_crosslinks
            yield tmp_item
        else:
            print("Nothing to Scrape!")

        for link in cleaned_links:
            yield scrapy.Request(link, callback=self.parse)
