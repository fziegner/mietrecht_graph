# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from .JuraBasicSpider import JuraBasicSpider
from .MietrechtEinfachSpider import MietrechtEinfachSpider
from .MietrechtLexikonSpider import MietrechtLexikonSpider
from .BGBSpider import BGBSpider
from .BMGEVSpider import BMGEVSpider
from .RechtslexikonSpider import RechtslexikonSpider

Spiders = [
    JuraBasicSpider,
    MietrechtEinfachSpider,
    MietrechtLexikonSpider,
    BGBSpider,
    BMGEVSpider,
    RechtslexikonSpider
]
