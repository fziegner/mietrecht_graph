from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from BauGraph.bauprofessor.spiders import *
from pathlib import Path

def go(dir=Path("./output")):
    if not isinstance(dir, Path):
        dir=Path(dir)
    if not dir.exists():
        dir.mkdir()

    process = CrawlerProcess(get_project_settings())
    process.crawl(BauprofessorSpider,o=dir/"bauprofessor.json")
    process.crawl(HausberaterSpider,o=dir/"hb.json")
    process.crawl(BeuthVOBSpider,o=dir/"baunormenlexikonvob.json")
    process.crawl(BeuthDINSpider,o=dir/"baunormenlexikondin.json")
    process.crawl(BeuthLexSpider,o=dir/"beutlex.json")
    process.crawl(HOAISpider,o=dir/"hoai.json")

    process.start()

