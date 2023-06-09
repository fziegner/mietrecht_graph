import scrapy
import re

class RechtslexikonItem(scrapy.Item):
    page_url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    crosslinks = scrapy.Field()

class RechtslexikonSpider(scrapy.Spider):

    name = "Rechtslexikon"
    start_urls = ["http://www.rechtslexikon.net/d/mietvertrag/mietvertrag.htm",
                    "http://www.rechtslexikon.net/d/mietspiegel/mietspiegel.htm",
                    "http://www.rechtslexikon.net/d/mietrecht/mietrecht.htm",
                    "http://www.rechtslexikon.net/d/mietkaution/mietkaution.htm",
                    "http://www.rechtslexikon.net/d/mieterh%C3%B6hung/mieterh%C3%B6hung.htm",
                    "http://www.rechtslexikon.net/d/mietaufhebungsklage/mietaufhebungsklage.htm",
                    "http://www.rechtslexikon.net/d/mietaufhebungsvereinbarung/mietaufhebungsvereinbarung.htm",
                    "http://www.rechtslexikon.net/d/mietausfallwagnis/mietausfallwagnis.htm",
                    "http://www.rechtslexikon.net/d/mieter/mieter.htm",
                    "http://www.rechtslexikon.net/d/miete/miete.htm",
                    "http://www.rechtslexikon.net/d/mieterabwesenheit/mieterabwesenheit.htm",
                    "http://www.rechtslexikon.net/d/wohnraummietvertrag/wohnraummietvertrag.htm"]
    custom_settings = {
        'DEPTH_LIMIT': 1
    }

    def parse(self, response):

        links = response.xpath("//*[@class='wikitext']//@href").getall()

        cleaned_links = []
        for link in links:
            if link.startswith("../../d"):
                cleaned_links.append("http://www.rechtslexikon.net/d" + link.split("d",1)[1])
            elif link.startswith("../"):
                cleaned_links.append("http://www.rechtslexikon.net/d/" + link.split("../",1)[1])
        cleaned_links = list(set(cleaned_links))

        element = response.xpath("//*[@class='wikitext']")
        if len(element) == 1:
            tmp_item = RechtslexikonItem()
            tmp_item['page_url'] =  str(response.url)
            tmp_item['title'] = response.xpath("string(//*[@class='pagetitle'])").get()
            selector = response.xpath("//*[@class='wikitext']//text()[not(ancestor::script)]").getall()
            tmp_item['text'] = re.sub("[\n\r\t]","","".join(selector).split(tmp_item['title'],1)[1].split("Vorheriger Fachbegriff")[0]).strip()
            tmp_item['crosslinks'] = cleaned_links
            yield tmp_item
        else:
            print("Nothing to Scrape!")

        for link in cleaned_links:
            yield scrapy.Request(link, callback=self.parse)
