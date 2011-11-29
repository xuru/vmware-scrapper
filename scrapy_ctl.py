#!/Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python

import sys
sys.path[0:0] = [
    '/Users/a872993/git/vmware-scrapper/eggs/Scrapy-0.12.0.2546-py2.7.egg',
    '/Users/a872993/git/vmware-scrapper/eggs/Jinja2-2.6-py2.7.egg',
    '/Users/a872993/git/vmware-scrapper/eggs/s01.scrapy-0.12.4-py2.7.egg',
    '/Users/a872993/git/vmware-scrapper/eggs/pytidylib-0.2.1-py2.7.egg',
    '/Users/a872993/git/vmware-scrapper/eggs/zope.schema-4.0.0-py2.7.egg',
    '/Users/a872993/git/vmware-scrapper/eggs/zope.interface-3.8.0-py2.7-macosx-10.6-intel.egg',
    '/Users/a872993/git/vmware-scrapper/eggs/Twisted-11.0.0-py2.7-macosx-10.6-intel.egg',
    '/Users/a872993/git/vmware-scrapper/eggs/simplejson-2.2.1-py2.7-macosx-10.6-intel.egg',
    '/Users/a872993/git/vmware-scrapper/eggs/zc.buildout-1.5.2-py2.7.egg',
    '/Users/a872993/git/vmware-scrapper/eggs/zc.recipe.egg-1.3.2-py2.7.egg',
    '/Users/a872993/git/vmware-scrapper/eggs/distribute-0.6.24-py2.7.egg',
    '/Users/a872993/git/vmware-scrapper/eggs/lxml-2.3.2-py2.7-macosx-10.6-intel.egg',
    '/Users/a872993/git/vmware-scrapper/eggs/six-1.0.0-py2.7.egg',
    '/Users/a872993/git/vmware-scrapper/eggs/zope.event-3.5.1-py2.7.egg',
    ]



import scrapy.conf
# fake inproject marker
scrapy.conf.settings.settings_module = True
# settings overrides
scrapy.conf.settings.overrides['USER_AGENT'] = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'
scrapy.conf.settings.overrides['HTTPCACHE_DIR'] = 'cache'
scrapy.conf.settings.overrides['DOWNLOAD_DELAY'] = 2
scrapy.conf.settings.overrides['ITEM_PIPELINES'] = ['visdk41.pipelines.VisdkPipeline']
scrapy.conf.settings.overrides['LOG_LEVEL'] = 'WARNING'
scrapy.conf.settings.overrides['HTTPCACHE_EXPIRATION_SECS'] = 0
scrapy.conf.settings.overrides['CRAWLSPIDER_FOLLOW_LINKS'] = True
scrapy.conf.settings.overrides['HTTPCACHE_ENABLED'] = True
scrapy.conf.settings.overrides['LOG_ENABLED'] = True
scrapy.conf.settings.overrides['DOWNLOAD_TIMEOUT'] = 20
scrapy.conf.settings.overrides['RANDOMIZE_DOWNLOAD_DELAY'] = True
scrapy.conf.settings.overrides['CONCURRENT_SPIDERS'] = 4
scrapy.conf.settings.overrides['EXTENSIONS'] = {'visdk41.extensions.GenConsts': 500}
scrapy.conf.settings.overrides['DUMP_DIR'] = 'dump'
scrapy.conf.settings.overrides['DEFAULT_ITEM_CLASS'] = 'visdk41.items.ManagedItem'
scrapy.conf.settings.overrides['DOC_DIR'] = 'docs'
scrapy.conf.settings.overrides['BOT_VERSION'] = '1.0'
scrapy.conf.settings.overrides['SPIDER_MODULES'] = ['visdk41.spiders']
scrapy.conf.settings.overrides['BOT_NAME'] = 'visdk41'
scrapy.conf.settings.overrides['OUTPUT_DIR'] = 'output'
scrapy.conf.settings.overrides['SPIDER_MIDDLEWARES'] = {'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': 543}
scrapy.conf.settings.overrides['DOWNLOADER_MIDDLEWARES'] = {'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 600, 'visdk41.middleware.LintMiddleware': 999, 'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': None}
scrapy.conf.settings.overrides['NEWSPIDER_MODULE'] = 'visdk41.spiders'


import scrapy.cmdline

scrapy.cmdline.execute(['scrapy', 'crawl', 'mo_spider'])
