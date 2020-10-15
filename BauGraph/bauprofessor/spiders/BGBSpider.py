import scrapy

class BGBItem(scrapy.Item):
    page_url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()

class BGBSpider(scrapy.Spider):

    name = "BGB"
    start_urls = ['https://www.gesetze-im-internet.de/bgb/__535.html',]

    def parse(self, response):

        links = [response.xpath("string(//*[@id='blaettern_weiter']/a/@href)").get()]

        cleaned_links = []
        for link in links:
            if link.startswith("_"):
                cleaned_links.append("http://www.gesetze-im-internet.de/bgb/" + link)

        element = response.xpath('//*[@id="blaettercontainer_12793"]')

        if len(element) == 1:
            tmp_item = BGBItem()
            tmp_item['page_url'] =  str(response.url)
            tmp_item['title'] = response.xpath("string(//*[@class='jnentitel'])").get()
            tmp_item['text'] = response.xpath("string(//*[@class='jnhtml'])").get()
            yield tmp_item
        else:
            print("Nothing to Scrape!")

        for link in cleaned_links:
            if not '581' in link:
                yield scrapy.Request(link, callback=self.parse)
