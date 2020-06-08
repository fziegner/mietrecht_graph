# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from .BauprofessorSpider import BauprofessorSpider
from .beuth_crawler import BeuthLexSpider
from .beuth_din_crawler import BeuthDINSpider
from .beuth_vob_crawler import BeuthVOBSpider
from .HausberaterSpider import HausberaterSpider
from .HOAI import HOAISpider

Spiders = [
    BauprofessorSpider,
    BeuthLexSpider,
    BeuthDINSpider,
    BeuthVOBSpider,
    HausberaterSpider,
    HOAISpider
]