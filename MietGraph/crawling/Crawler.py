from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from MietGraph.crawling.spiders import *
from pathlib import Path

def go(dir=Path("./output")):
    if not isinstance(dir, Path):
        dir=Path(dir)
    if not dir.exists():
        dir.mkdir()

    process = CrawlerProcess(get_project_settings())
    process.crawl(JuraBasicSpider,o=dir/"jurabasic.json")
    process.crawl(MietrechtEinfachSpider,o=dir/"mietrechteinfach.json")
    process.crawl(MietrechtLexikonSpider,o=dir/"mietrechtlexikon.json")
    process.crawl(BGBSpider,o=dir/"bgb.json")
    process.crawl(BMGEVSpider,o=dir/"bmgev.json")
    process.crawl(RechtslexikonSpider,o=dir/"rechtslexikon.json")

    process.start()
