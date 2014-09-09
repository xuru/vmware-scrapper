from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

class Base(BaseSpider):
    VIM = "http://pubs.vmware.com/vsphere-55/topic/com.vmware.wssdk.apiref.doc/"
    SMS = "http://pubs.vmware.com/vsphere-55/topic/com.vmware.wssdk.smssdk.doc/"

    def __init__(self):
        super(Base, self).__init__()
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
        yield self.object_class().parse(response)
