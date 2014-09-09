
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

import os.path
import urllib
from visdk41.items import EnumObject
from .urls import SMS, VIM

class Enumpider(BaseSpider):
    name = 'enum_spider'
    start_urls = [
                  SMS + "index-e_types.html",
                  VIM + "index-e_types.html"
                 ]

    def __init__(self):
        BaseSpider.__init__(self)
        self.verificationErrors = []

    def __del__(self):
        print self.verificationErrors

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        urls = hxs.select("//div[@class]//a[@href]")
        for url in urls:
            basename = url.select('./@href').extract()[0]
            url = '/'.join([response.url.rsplit('/', 1)[0], basename])
            yield Request(url, callback=self.parse_page)

    def parse_page(self, response):
        self.log('parse_page: %s' % response.url)
        yield EnumObject().parse(response)
