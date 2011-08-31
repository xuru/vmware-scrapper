
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

from visdk41.items import EnumObject
from visdk41.settings import config

class EnumSpider(BaseSpider):
    name = 'enum_spider'
    start_urls = [ "http://www.vmware.com/support/developer/vc-sdk/visdk41pubs/ApiReference/index-e_types.html" ]
    
    def __init__(self):
        BaseSpider.__init__(self)
        self.verificationErrors = []
        
    def __del__(self):
        print self.verificationErrors
        BaseSpider.__del__(self)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        urls = hxs.select("//div[@class]//a[@href]")
        for url in urls:
            url = url.select('./@href').extract()[0] 
            url = config.get('general', 'base_url') + url
            yield Request(url, callback=self.parse_page)
                
    def parse_page(self, response):
        self.log('parse_page: %s' % response.url)
        yield EnumObject().parse(response)
