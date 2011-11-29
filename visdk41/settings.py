# Scrapy settings for visdk41 project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
BOT_NAME = 'visdk41'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['visdk41.spiders']
NEWSPIDER_MODULE = 'visdk41.spiders'
DEFAULT_ITEM_CLASS = 'visdk41.items.ManagedItem'
#USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
USER_AGENT = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'

CRAWLSPIDER_FOLLOW_LINKS = True

# --- Log ---
LOG_ENABLED = True
LOG_LEVEL='WARNING'


# --- Cache ---
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'cache'

# --- Extensions ---
EXTENSIONS = {
    'visdk41.extensions.GenConsts': 500,
}

# --- Middlewares ---
SPIDER_MIDDLEWARES = {
    'scrapy.contrib.spidermiddleware.referer.RefererMiddleware':543,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware':None,
    'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware':600,
    'visdk41.middleware.LintMiddleware':999,
}

ITEM_PIPELINES = [
    'visdk41.pipelines.VisdkPipeline'
]

# --- Concurrent ---
CONCURRENT_SPIDERS=4

# --- Delay ---
DOWNLOAD_DELAY = 2
DOWNLOAD_TIMEOUT = 20
RANDOMIZE_DOWNLOAD_DELAY = True

# --- app specific ---
OUTPUT_DIR = 'output'
DOC_DIR = 'docs'

DUMP_DIR = "dump"
