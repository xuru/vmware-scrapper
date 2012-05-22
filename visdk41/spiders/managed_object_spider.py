
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

import os.path
from visdk41.items import ManagedObject
from ConfigParser import ConfigParser
config = ConfigParser()
config.read( os.path.join(os.path.abspath(os.path.dirname(__file__)), '..','..',  'visdk41.cfg'))

class MOSpider(BaseSpider):
    name = 'mo_spider'
    start_urls = [ "http://vijava.sourceforge.net/vSphereAPIDoc/ver5/ReferenceGuide/index-mo_types.html" ]
    
    def __init__(self):
        BaseSpider.__init__(self)
        self.verificationErrors = []
        
    def __del__(self):
        print self.verificationErrors

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        urls = hxs.select("//div[@class]//a[@href]")
        for url in urls:
            url = url.select('./@href').extract()[0] 
            url = config.get('general', 'base_url') + url
            yield Request(url, callback=self.parse_page)
                
    def parse_page(self, response):
        self.log('parse_page: %s' % response.url)
        yield ManagedObject().parse(response)
